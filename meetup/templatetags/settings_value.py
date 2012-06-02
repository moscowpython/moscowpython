from django import template
from django.conf import settings

register = template.Library()

@register.assignment_tag
def get_settings_value(name):
    try:
        return settings.__getattr__(name)
    except AttributeError:
        return ""