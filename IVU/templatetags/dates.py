"""
Contains common template filters for datetime fields of objects.
"""

from django import template

from IVU.requests import IVUDatedRequest

register = template.Library()


@register.filter(expects_localtime=True)
def ivu_strftime(value):
    """Returns parsed date string in irena facade accepted date pattern.
    """
    fmt = IVUDatedRequest.fmt
    return value.strftime(fmt)
