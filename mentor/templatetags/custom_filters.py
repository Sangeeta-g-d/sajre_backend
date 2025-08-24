# mentor/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def remove_parentheses(value):
    """Remove text in parentheses from the string"""
    if '(' in value and ')' in value:
        return value.split('(')[0].strip()
    return value

