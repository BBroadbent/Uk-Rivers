from django import template
from django.utils import formats
from dateutil import parser

register = template.Library()

@register.filter
def dateString(value, arg=None):
    """Format a date according to the given format."""
    try:
        value = parser.parse(value)
    except Exception as e:
        print(e)
        return ''
    if value in (None, ''):
        return ''
    try:
        return formats.date_format(value, arg)
    except AttributeError:
        try:
            return format(value, arg)
        except AttributeError:
            return ''