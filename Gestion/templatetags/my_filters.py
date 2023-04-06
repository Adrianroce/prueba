from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='times') 
def times(number):
    return range(number)

@register.filter(name='access') 
def access(d, key):
    return d[key].img.url

@register.filter(name='Toint') 
def Toint(n):
    return int(n)

@register.filter(name='tostrDecimal') 
@stringfilter
def tostrDecimal(str_float):
    return str_float.replace(",", ".")