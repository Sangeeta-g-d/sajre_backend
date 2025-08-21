from django import template
import re
register = template.Library()

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def remove_parentheses(value):
    """Remove text inside parentheses (and the parentheses themselves)."""
    if not isinstance(value, str):
        return value
    return re.sub(r"\(.*?\)", "", value).strip()