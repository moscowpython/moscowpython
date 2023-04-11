from __future__ import annotations

from django.urls import path, re_path
from django.views.generic import RedirectView

from .views import LegacyEventPage, LegacyTalkPage

urlpatterns = [
    path('meetups/', RedirectView.as_view(url='/meetup/'), name='old-events'),
    path('meetups/<int:pk>/', LegacyEventPage.as_view(), name='old-event'),
    re_path(r'^meetups/(?P<event_id>\d+)/(?P<talk_slug>[\w-]+)/$', LegacyTalkPage.as_view(), name='old-talk'),
]
