import datetime


def session_password_key():
    return 'stored_password'


def fetch_credentials(request):
    username = getattr(request.user, 'authentication_field', None)

    if not username:
        raise ValueError(f'invalid authentication field value - got {username}')

    password = request.session.get(session_password_key())
    return username, password


def alina_strftime(date):
    date = date.strftime('%Y-%m-%d')
    return date


def timetable_alina_strftime(timetable):
    date = datetime.date(year=timetable.year, month=timetable.month, day=1)
    date_str = alina_strftime(date)
    return date_str
