"""
Contains filter which returns aware datetime object in common local date format. "%H:%M %d.%m.%Yr.".
"""
from django import template
from django.utils import timezone

from utils.dates import REPRESENTATIVE_DATE_FORMAT

register = template.Library()


@register.filter(expects_localtime=True)
def represent_date(value):
    date_local = value.strftime(REPRESENTATIVE_DATE_FORMAT)
    return date_local


@register.filter()
def represent_hour(value):
    fmt = '%H:%M'
    local = timezone.localtime(value).strftime(fmt)
    return local
