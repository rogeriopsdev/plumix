# plumixapp/templatetags/form_extras.py
from django import template

register = template.Library()

@register.filter
def attr(obj, name):
    """Permite acessar um atributo dinamicamente: {{ obj|attr:'campo' }}"""
    return getattr(obj, name, '')
