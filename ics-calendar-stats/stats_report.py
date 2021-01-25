import logging
from collections import defaultdict

from calendar_event import CalendarEvent
from stats_config import StatsConfig
from utils.auto_str import auto_str


CATEGORY_DID_NOT_ACCEPT = 'Did not accept'
CATEGORY_UNCATEGORIZED = 'Uncategorized'
CATEGORY_ONE_ON_ONE = '1:1'

@auto_str
class EnrichedEvent:
    def __init__(self, event: CalendarEvent):
        self.event = event
        self.excluded = False
        self.category = CATEGORY_UNCATEGORIZED
        self.duration = self.event.duration_minutes()
        self.event_day = self.event.day_str()
        self.event_week = self.event.week_str()

    def check_response(self, owner: str):
        for attendee in self.event.attendees:
            if attendee.email == owner:
                logging.debug(attendee)
                if not attendee.partstat == 'ACCEPTED':
                    self.excluded = True
                break

    def is_1on1(self):
        return len(self.event.attendees) == 2

    def categorize(self, config):
        detected_category = None
        for category, words in config.category_keywords.items():
            for word in words:
                if word in self.event.summary:
                    detected_category = category
                    break
            if detected_category:
                break
        if detected_category:
            self.category = detected_category
            return

        # Use other detection methods for standard categories
        # If there are only 2 people — that's a 1:1, doh...
        if self.is_1on1():
            self.category = CATEGORY_ONE_ON_ONE

    def format_string(self):
        return 'start_time={}, end_time={}, excluded={:1}, category={:15} {}'.format(
            self.event.start_time,
            self.event.end_time,
            self.excluded,
            self.category,
            self.event.summary,
        )

    def __repr__(self):
        return self.__str__()


class StatsReport:
    def __init__(self, args, config: StatsConfig):
        self.args = args
        self.config = config
        self.events = []

    def process_event(self, event):
        enriched_event = EnrichedEvent(event)
        enriched_event.check_response(self.config.mailbox)
        enriched_event.categorize(self.config)
        self.events.append(enriched_event)

    def print_events(self):
        sorted_events = sorted(self.events, key=lambda item: item.event.start_time)
        for event in sorted_events:
            print(event.format_string())

    def get_all_categories(self):
        categories = list(self.config.category_keywords.keys())
        if CATEGORY_ONE_ON_ONE not in categories:
            categories.append(CATEGORY_ONE_ON_ONE)
        categories += [CATEGORY_UNCATEGORIZED, CATEGORY_DID_NOT_ACCEPT]
        return categories

    def get_empty_daily_stats(self):
        all_categories = self.get_all_categories()
        empty_stats = {c: 0 for c in all_categories}
        return empty_stats

    def collect_by_day_by_category(self):
        """Returns event time aggregated by day or by week depending on the args"""
        empty_stats = self.get_empty_daily_stats()
        by_day_by_category = defaultdict(lambda: empty_stats.copy())

        sorted_events = sorted(self.events, key=lambda item: item.event.start_time)
        for event in sorted_events:
            if event.excluded:
                category = CATEGORY_DID_NOT_ACCEPT
            else:
                category = event.category
            time_bucket = event.event_week if self.args.weekly else event.event_day
            by_day_by_category[time_bucket][category] += event.duration
        return by_day_by_category

    def print_by_category(self):
        by_day_by_category = self.collect_by_day_by_category()
        totals = self.get_empty_daily_stats()
        total_time = 0

        for _, categories in by_day_by_category.items():
            for category, minutes in categories.items():
                totals[category] += minutes
                total_time += minutes

        sorted_by_category = sorted(totals.items(), key=lambda item: item[1])

        for category, time in sorted_by_category:
            print('{:15} {:>3} mins (== {:.2f} hrs)'.format(category, time, time / 60))
        print('\nTotal time in meetings: {} mins (== {:.2f} hrs)'.format(total_time, total_time / 60))

    def print_summary_csv(self):
        headers = ','.join(self.get_all_categories())
        print('{},{}'.format(
            'Week' if self.args.weekly else 'Day',
            headers))

        by_day_by_category = self.collect_by_day_by_category()
        for day, categories in by_day_by_category.items():
            numbers = categories.values()
            if self.args.hours:
                numbers = [m / 60 for m in numbers]
            numbers_str = ','.join(map(str, numbers))
            row = '{},{}'.format(day, numbers_str)
            print(row)
