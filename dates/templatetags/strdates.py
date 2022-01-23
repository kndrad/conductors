"""
Contains template tags which display datetime objects in any given string format.
"""

from django import template
from django.utils import timezone


register = template.Library()


@register.filter(expects_localtime=True)
def full_date(value):
    return value.strftime("%H:%M %d.%m.%Yr.")


@register.filter()
def time_only(value):
    return timezone.localtime(value).strftime("%H:%M")


@register.filter()
def date_only(value):
    return timezone.localtime(value).strftime("%d.%m.%Yr.")
