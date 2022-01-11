"""
Contains common template filters for datetime fields of objects.
"""

from django import template

from IVU.requests import IVURequestWithDateString

register = template.Library()


@register.filter(expects_localtime=True)
def ivu_strftime(value):
    """Returns parsed date string in irena facade accepted date pattern.
    """
    fmt = IVURequestWithDateString.fmt
    return value.strftime(fmt)
