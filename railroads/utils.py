import datetime


def format_date_for_engine(date: datetime.datetime):
    hour = date.strftime('%H:%M')
    date = date.strftime('%d.%m.%Y')
    return hour, date
