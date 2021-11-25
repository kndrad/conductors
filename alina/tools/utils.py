import datetime

ALINA_DATE_FORMAT = '%Y-%m-%d'
STORED_PASSWORD_KEY = 'stored_password'


def credentials_from_request(request):
    email = request.user.email
    password = request.session.get(STORED_PASSWORD_KEY)
    return email, password


def parse_alina_date(date):
    date = date.strftime(ALINA_DATE_FORMAT)
    return date


def parse_alina_timetable_date(timetable):
    date = datetime.date(year=timetable.year, month=timetable.month, day=1)
    formatted_date = parse_alina_date(date)
    return formatted_date
