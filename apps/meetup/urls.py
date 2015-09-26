# coding: utf-8
from django.conf.urls import patterns, url, include
from apps.meetup import views


urlpatterns = patterns('',
    url('^$', views.IndexPage.as_view(), name='index'),
    url('^about/$', views.AboutPage.as_view(), name='about'),
    url('^live/$', views.LivePage.as_view(), name='live'),
    url('^meetup/$', views.EventsList.as_view(), name='events'),
    url('^meetup/(?P<number>\d+)/$', views.EventPage.as_view(), name='event'),
    url('^meetup/(?P<event_number>\d+)/(?P<talk_slug>[\w-]+)/$', views.TalkPage.as_view(), name='talk'),
    url('^speakers/$', views.SpeakerList.as_view(), name='speakers'),
    url('^speakers/(?P<slug>[\w-]+)/$', views.SpeakerPage.as_view(), name='speaker'),
    url('^tutorials/$', views.TutorialList.as_view(), name='tutorials'),
    url('^tutorials/(?P<slug>[\w-]+)/$', views.TutorialPage.as_view(), name='tutorial'),
    url('^vote/(?P<talk_id>\d+)/$', views.ajax_vote, name='vote'),
    url('^prize/$', views.VoteResults.as_view(), name='vote-results'),

    # legacy
    url('', include('apps.meetup.legacy.urls')),
)
