# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from meetup.views import EventPage, TalkPage, SpeakerPage
from views import IndexPage, EventsList, AboutPage, LivePage, ajax_subscribe
from django.views.generic.base import TemplateView


urlpatterns = patterns('',
    url('^$', IndexPage.as_view(), name='index'),
    url('^subscribe/$', ajax_subscribe, name='subscribe'),
    url('^about/$', AboutPage.as_view(), name='about'),
    url('^live/$', LivePage.as_view(), name='live'),
    url('^meetup/$', EventsList.as_view(), name='events'),
    url('^meetup/(?P<number>\d+)/$', EventPage.as_view(), name='event'),
    url('^meetup/(?P<event_number>\d+)/(?P<talk_slug>[\w-]+)/$', TalkPage.as_view(), name='talk'),
    url('^speakers/$', TemplateView.as_view(template_name='speakers.html'), name='speakers'),
    url('^speakers/(?P<slug>[\w-]+)/$', SpeakerPage.as_view(), name='speaker'),
    url('', include('meetup.legacy.urls')),
)
