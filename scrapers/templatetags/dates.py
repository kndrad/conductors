"""
Contains common template filters for datetime fields of objects.
"""

from django import template

from scrapers.models import REQUEST_DATE_FMT

register = template.Library()


@register.filter(expects_localtime=True)
def facade_strftime(value):
    """Returns parsed date string in irena facade accepted date pattern.
    """
    return value.strftime(REQUEST_DATE_FMT)
