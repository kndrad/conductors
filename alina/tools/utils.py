import datetime

STORED_PASSWORD_KEY = 'stored_password'


def get_session_credentials(request):
    email = request.user.email
    password = request.session.get(STORED_PASSWORD_KEY)
    return email, password


def alina_strftime(date):
    date = date.strftime('%Y-%m-%d')
    return date


def timetable_alina_strftime(timetable):
    date = datetime.date(year=timetable.year, month=timetable.month, day=1)
    date_str = alina_strftime(date)
    return date_str
