"""
Contains filter which returns aware datetime object in common local date format. "%H:%M %d.%m.%Yr.".
"""
from django import template
from django.utils import timezone

from utils.dates import StringDateFormat

register = template.Library()


@register.filter(expects_localtime=True)
def full_date(value):
    fmt = StringDateFormat.FULL.value
    local = value.strftime(fmt)
    return local


@register.filter()
def hour_only(value):
    fmt = StringDateFormat.TIME.value
    local = timezone.localtime(value).strftime(fmt)
    return local


@register.filter()
def date_tracked(value):
    fmt = StringDateFormat.TRACKED.value
    local = timezone.localtime(value).strftime(fmt)
    return local
