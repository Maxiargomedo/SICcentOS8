# filepath: c:\SIC final\compras_auth\sic_autorizaciones\templatetags\custom_filters.py
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})