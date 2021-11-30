"""
Contains filter which returns aware datetime object in common local date format. "%H:%M %d.%m.%Yr.".
"""
from django import template

from utils.dates import REPRESENTATIVE_DATE_FORMAT

register = template.Library()


@register.filter(expects_localtime=True)
def represent_date(value):
    date_local = value.strftime(REPRESENTATIVE_DATE_FORMAT)
    return date_local
