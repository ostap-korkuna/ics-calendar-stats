from typing import List

import dateutil.parser
from dateutil import tz
from ics import Calendar

from calendar_event import CalendarEvent
from stats_config import StatsConfig
from stats_report import StatsReport
from utils.ics_cleanup import cleanup_ics_string


class CalendarStats:
    def __init__(self, args):
        self.args = args
        self.file = self.args.file
        self.date_range = [dateutil.parser.parse(dt).replace(tzinfo=tz.tzlocal()) for dt in self.args.date_range]

    def load_events(self):
        cal_file = open(self.file, 'r')
        file_contents = cal_file.read()
        clean_file = cleanup_ics_string(file_contents)
        calendar = Calendar(clean_file)

        events = []
        for event in calendar.events:
            summary = event.name
            start_date = event.begin.datetime
            end_date = event.end.datetime
            attendees = event.attendees
            if not self.date_range or self.date_range[0] <= start_date < self.date_range[1]:
                events.append(CalendarEvent(summary, start_date, end_date, attendees))

        cal_file.close()
        return events

    def generate_report(self, events: List[CalendarEvent], config: StatsConfig):
        report = StatsReport(self.args, config)
        for event in events:
            report.process_event(event)
        return report

    def run(self, config: StatsConfig):
        events = self.load_events()
        report = self.generate_report(events, config)
        if self.args.csv:
            report.print_daily_summary_csv()
            pass
        else:
            report.print_events()
            print('\n')
            report.print_by_category()
