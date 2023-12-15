from __future__ import annotations

from django.urls import include, path, re_path

from .views import (
    AboutPage,
    EventPage,
    EventsList,
    IndexPage,
    LivePage,
    SpeakerList,
    SpeakerPage,
    TalkPage,
    TutorialList,
    TutorialPage,
    VoteResults,
    ajax_vote,
    ajax_set_embedly_data,
)

urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('about/', AboutPage.as_view(), name='about'),
    path('live/', LivePage.as_view(), name='live'),
    path('meetup/', EventsList.as_view(), name='events'),
    path('meetup/<int:number>/', EventPage.as_view(), name='event'),
    re_path(r'^meetup/(?P<event_number>\d+)/(?P<talk_slug>[\w-]+)/$', TalkPage.as_view(), name='talk'),
    path('speakers/', SpeakerList.as_view(), name='speakers'),
    re_path(r'^speakers/(?P<slug>[\w-]+)/$', SpeakerPage.as_view(), name='speaker'),
    path('tutorials/', TutorialList.as_view(), name='tutorials'),
    re_path(r'^tutorials/(?P<slug>[\w-]+)/$', TutorialPage.as_view(), name='tutorial'),
    path('vote/<int:talk_id>/', ajax_vote, name='vote'),
    path('set-embedly-data/<int:talk_id>/<str:field_name>', ajax_set_embedly_data, name='set-embedly-data'),
    path('prize/', VoteResults.as_view(), name='vote-results'),
    # legacy
    path('', include('apps.meetup.legacy.urls')),
]
