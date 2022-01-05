"""
Contains common template filters for datetime fields of objects.
"""

from django import template

from facades.models import ACCEPTED_DATETIME_FORMAT

register = template.Library()


@register.filter(expects_localtime=True)
def facade_strftime(value):
    """Returns parsed date string in irena facade accepted date pattern.
    """
    return value.strftime(ACCEPTED_DATETIME_FORMAT)
