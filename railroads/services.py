import datetime

from dateutil.parser import parse as dateutil_parse
from django.utils.timezone import make_aware, is_aware

from railroads.engines import RailroadSearchEngine
from .models import PublicRailroadTrain
from .utils import format_date_for_engine


def search_train(departure_station, arrival_station, date):
    if not isinstance(date, datetime.datetime):
        raise ValueError(f'date must be instance of {datetime.datetime}.')

    search_engine = RailroadSearchEngine(hide_actions=True)
    hour, date = format_date_for_engine(date)
    results = search_engine.run_searching(departure_station, arrival_station, hour, date)

    for result in results:
        departure_date = make_aware(dateutil_parse(
            f"{result['start_date']['date']} {result['start_date']['hour']}", dayfirst=True)
        )
        arrival_date = make_aware(dateutil_parse(
            f"{result['end_date']['date']} {result['end_date']['hour']}", dayfirst=True)
        )
        train, _ = PublicRailroadTrain.objects.get_or_create(
            number=result['number'],
            carrier=result['carrier'],
            departure_date=departure_date,
            departure_station=result['start_waypoint']['station'],
            departure_platform=result['start_waypoint']['platform'],
            arrival_date=arrival_date,
            arrival_station=result['end_waypoint']['station'],
            arrival_platform=result['end_waypoint']['platform']
        )
        yield train


def arriving_trains(departure_station, arrival_station, date):
    if not is_aware(date):
        date = make_aware(date)
    engine_date = date

    trains = set()
    while not trains:
        engine_date -= datetime.timedelta(minutes=15)
        for train in search_train(departure_station, arrival_station, engine_date):
            if train.arrival_date < date:
                trains.add(train)

    return trains


def departing_trains(departure_station, arrival_station, date):
    if not is_aware(date):
        date = make_aware(date)
    engine_date = date

    trains = set()
    while not trains:
        for train in search_train(departure_station, arrival_station, engine_date):
            if train.departure_date > date:
                trains.add(train)

        engine_date += datetime.timedelta(minutes=5)

    return trains


def nearest_arriving_train(date, departure_station, arrival_station):
    if not is_aware(date):
        date = make_aware(date)

    trains = arriving_trains(departure_station, arrival_station, date)
    dates = [train.arrival_date for train in trains]
    arrival_date = min(dates, key=lambda x: abs(x - date))
    train = next(train for train in trains if train.arrival_date == arrival_date)
    return train


def nearest_departing_train(date, departure_station, arrival_station):
    if not is_aware(date):
        date = make_aware(date)

    trains = departing_trains(departure_station, arrival_station, date)
    dates = [train.departure_date for train in trains]
    departure_date = min(dates, key=lambda x: abs(date - x))
    train = next(train for train in trains if train.departure_date == departure_date)
    return train
