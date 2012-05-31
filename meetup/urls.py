# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from views import IndexPage

urlpatterns = patterns('',
    url('^$', IndexPage.as_view(), name='index'),
    url('^event/(?P<pk>\d+)/$', TemplateView.as_view(template_name='index.html'), name='event'),
    url('^talk/(?P<pk>\d+)/$', TemplateView.as_view(template_name='index.html'), name='talk'),
)