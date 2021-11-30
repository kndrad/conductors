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


class ICalConvertable:
    @abc.abstractmethod
    def ical_component(self):
        return NotImplemented
