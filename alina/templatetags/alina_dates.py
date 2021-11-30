"""
Contains common template filters for datetime fields of objects.
"""

from django import template

from alina.tools.utils import parse_date_for_alina

register = template.Library()


@register.filter(expects_localtime=True)
def date_for_alina(value):
    """Returns parsed date string in alina date pattern.
    """
    parsed_date = parse_date_for_alina(value)
    return parsed_date
