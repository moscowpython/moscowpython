# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from meetup.views import EventPage, TalkPage
from views import IndexPage

urlpatterns = patterns('',
    url('^$', IndexPage.as_view(), name='index'),
    url('^events/(?P<pk>\d+)/$', EventPage.as_view(), name='event'),
    url('^talks/(?P<pk>\d+)/$', TalkPage.as_view(), name='talk'),
)