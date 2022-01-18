import abc
import datetime

from dateutil.parser import parse as dateutil_parse
from django.utils.timezone import make_aware, is_aware

from trains.services import SearchingTrainScheduleService
from .models import Train


def search_train(date, departure, arrival):
    if not isinstance(date, datetime.datetime):
        raise ValueError(f'date must be instance of {datetime.datetime}.')

    service = SearchingTrainScheduleService(hide_actions=False)
    hour, date = date.strftime('%H:%M'), date.strftime('%d.%m.%Y')
    trains = service.get_trains(date, hour, departure, arrival)

    for parsed in trains:
        departure_date = make_aware(dateutil_parse(
            f"{parsed['start_date']['date']} {parsed['start_date']['hour']}", dayfirst=True)
        )
        arrival_date = make_aware(dateutil_parse(
            f"{parsed['end_date']['date']} {parsed['end_date']['hour']}", dayfirst=True)
        )
        train, _ = Train.objects.get_or_create(
            number=parsed['number'],
            carrier=parsed['carrier'],
            departure_date=departure_date,
            departure_station=parsed['start_waypoint']['station'],
            departure_platform=parsed['start_waypoint']['platform'],
            arrival_date=arrival_date,
            arrival_station=parsed['end_waypoint']['station'],
            arrival_platform=parsed['end_waypoint']['platform']
        )
        yield train


def trains_before(date, depature, arrival):
    if not is_aware(date):
        date = make_aware(date)

    engine_date = date
    trains = set()

    while not trains:
        engine_date -= datetime.timedelta(minutes=15)
        for train in search_train(date, depature, arrival):
            if train.arrival_date < date:
                trains.add(train)

    return trains


def trains_after(date, depature, arrival):
    if not is_aware(date):
        date = make_aware(date)

    engine_date = date
    trains = set()

    while not trains:
        for train in search_train(date, depature, arrival):
            if train.departure_date > date:
                trains.add(train)
        engine_date += datetime.timedelta(minutes=5)

    return trains


class NearestTrain:
    journey_period = None  # 'arrival' or 'departure'

    def __init__(self, date):
        if not is_aware(date):
            date = make_aware(date)
        self._date = date

    @abc.abstractmethod
    def sort_dates(self, dates):
        pass

    def inspect(self, trains):
        periodic_date = f'{self.journey_period}_date'
        dates = [getattr(train, periodic_date) for train in trains]
        closest_date = self.sort_dates(dates)
        return next(train for train in trains if getattr(train, periodic_date) == closest_date)


class DateArrivingTrain(NearestTrain):
    journey_period = 'arrival'

    def sort_dates(self, dates):
        return min(dates, key=lambda x: abs(x - self._date))


class DateDepartingTrain(NearestTrain):
    journey_period = 'departure'

    def sort_dates(self, dates):
        return min(dates, key=lambda x: abs(self._date - x))


# def nearest_arriving_train(date, departure_station, arrival_station):
#     if not is_aware(date):
#         date = make_aware(date)
#
#     trains = arriving_trains(departure_station, arrival_station, date)
#     dates = [train.arrival_date for train in trains]
#     arrival_date = min(dates, key=lambda x: abs(x - date))
#     return next(train for train in trains if train.arrival_date == arrival_date)
#
#
# def nearest_departing_train(date, departure_station, arrival_station):
#     if not is_aware(date):
#         date = make_aware(date)
#
#     trains = departing_trains(departure_station, arrival_station, date)
#     dates = [train.departure_date for train in trains]
#     departure_date = min(dates, key=lambda x: abs(date - x))
#     return next(train for train in trains if train.departure_date == departure_date)
