import logging
from collections import defaultdict

from calendar_event import CalendarEvent
from stats_config import StatsConfig
from utils.auto_str import auto_str


CATEGORY_DID_NOT_ACCEPT = 'Did not accept'
CATEGORY_UNCATEGORIZED = 'Uncategorized'

@auto_str
class EnrichedEvent:
    def __init__(self, event: CalendarEvent):
        self.event = event
        self.excluded = False
        self.category = CATEGORY_UNCATEGORIZED
        self.duration = self.event.duration_minutes()
        self.event_day = self.event.day_str()

    def check_response(self, owner: str):
        for attendee in self.event.attendees:
            if attendee.email == owner:
                logging.debug(attendee)
                if not attendee.partstat == 'ACCEPTED':
                    self.excluded = True
                break

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
        return list(self.config.category_keywords.keys()) + [CATEGORY_UNCATEGORIZED, CATEGORY_DID_NOT_ACCEPT]

    def get_empty_daily_stats(self):
        all_categories = self.get_all_categories()
        empty_stats = {c: 0 for c in all_categories}
        return empty_stats

    def collect_by_day_by_category(self):
        empty_stats = self.get_empty_daily_stats()
        by_day_by_category = defaultdict(lambda: empty_stats.copy())

        sorted_events = sorted(self.events, key=lambda item: item.event.start_time)
        for event in sorted_events:
            if event.excluded:
                category = CATEGORY_DID_NOT_ACCEPT
            else:
                category = event.category
            by_day_by_category[event.event_day][category] += event.duration
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

    def print_daily_summary_csv(self):
        headers = ','.join(self.get_all_categories())
        print('Date,{}'.format(headers))

        by_day_by_category = self.collect_by_day_by_category()
        for day, categories in by_day_by_category.items():
            numbers = ','.join(map(str, categories.values()))
            row = '{},{}'.format(day, numbers)
            print(row)
