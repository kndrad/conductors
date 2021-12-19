"""
Contains common template filters for datetime fields of objects.
"""

from django import template

from alina.tools.utils import alina_strftime

register = template.Library()


@register.filter(expects_localtime=True)
def alina_date_str(value):
    """Returns parsed date string in alina date pattern.
    """
    date = alina_strftime(value)
    return date
