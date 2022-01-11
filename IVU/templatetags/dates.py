"""
Contains common template filters for datetime fields of objects.
"""

from django import template

from IVU.api.requests import IVURequestWithDateValue

register = template.Library()


@register.filter(expects_localtime=True)
def ivu_strftime(value):
    """Returns parsed date string in irena facade accepted date pattern.
    """
    fmt = IVURequestWithDateValue.fmt
    return value.strftime(fmt)
