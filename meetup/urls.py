# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    url('^$', TemplateView.as_view(template_name='index.html'))
)