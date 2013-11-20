# coding: utf-8
"""
    Based on deprecated django.contrib.markup
"""
from django.utils.encoding import force_str, force_bytes, force_text
import markdown as mdlib
from docutils.core import publish_parts
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def markdown(value):
    return mark_safe(mdlib.markdown(force_str(value), safe_mode=True))


@register.filter(is_safe=True)
def restructuredtext(value):
    parts = publish_parts(source=force_bytes(value), writer_name="html4css1")
    return mark_safe(force_text(parts["fragment"]))
