import abc
import datetime

import icalendar


class TriggeredAlarm(icalendar.Alarm):
    """TriggeredAlarm is a icalendar.Alarm component object with 'trigger' function.
    """

    def __init__(self, *args, **timespan):
        super().__init__(*args, **timespan)
        self.add('action', 'DISPLAY')

        timespan = {span: -abs(time) for span, time in timespan.items() if time > 0}

        trigger = datetime.timedelta(**timespan)
        self.add('trigger', trigger)


class ICalComponentable:
    """Interface for any instance that can be converted to ical event or calendar component.
    """
    @abc.abstractmethod
    def to_ical_component(self):
        return NotImplemented
