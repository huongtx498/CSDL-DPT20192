from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)[1]

@register.filter(name='range') 
def filter_range(start, end):   
    return range(start, end)