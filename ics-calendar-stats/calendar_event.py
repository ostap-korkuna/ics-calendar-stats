from utils.auto_str import auto_str


@auto_str
class CalendarEvent:
    def __init__(self, summary, start_time, end_time, attendees):
        self.summary = summary
        self.start_time = start_time
        self.end_time = end_time
        self.attendees = attendees

    def duration_minutes(self):
        time_delta = (self.end_time - self.start_time)
        seconds = time_delta.total_seconds()
        return int(seconds / 60)

    def day_str(self):
        return self.start_time.strftime('%Y-%m-%d')

    def __repr__(self):
        return self.__str__()
