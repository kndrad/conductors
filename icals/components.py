import abc

import datetime

import icalendar


class ICalTriggeredAlarm(icalendar.Alarm):
    def __init__(self, *args, **timespan):
        super().__init__(*args, **timespan)
        self.add('action', 'DISPLAY')

        trigger = datetime.timedelta(**{span: -abs(time) for span, time in timespan.items() if time > 0})
        self.add('trigger', trigger)


class ICalConvertable:
    @abc.abstractmethod
    def to_ical_component(self):
        pass
