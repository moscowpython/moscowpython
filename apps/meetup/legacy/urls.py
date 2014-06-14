# coding: utf-8
from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from .views import LegacyTalkPage, LegacyEventPage


urlpatterns = patterns('',
    url('^meetups/$', RedirectView.as_view(url='/meetup/'), name='old-events'),
    url('^meetups/(?P<pk>\d+)/$', LegacyEventPage.as_view(), name='old-event'),
    url('^meetups/(?P<event_id>\d+)/(?P<talk_slug>[\w-]+)/$', LegacyTalkPage.as_view(), name='old-talk'),
)

