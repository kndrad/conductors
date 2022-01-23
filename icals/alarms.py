import datetime

import icalendar


class ICalTriggeredAlarm(icalendar.Alarm):
    """ Alarm component set to timespans kwargs provided in a constructor. Contains 'trigger'.
    """
    def __init__(self, *args, **timespans):
        super().__init__(*args, **timespans)
        self.add('action', 'DISPLAY')

        trigger = datetime.timedelta(**{span: -abs(time) for span, time in timespans.items() if time > 0})
        self.add('trigger', trigger)
