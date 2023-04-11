from __future__ import annotations

from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView

from ..models import Event, Talk


class LegacyEventPage(RedirectView):
    def get_redirect_url(self, **kwargs):
        event = get_object_or_404(Event, pk=kwargs['pk'])
        return event.get_absolute_url()


class LegacyTalkPage(RedirectView):
    def get_redirect_url(self, **kwargs):
        talk = get_object_or_404(Talk, slug=kwargs['talk_slug'])
        return talk.get_absolute_url()
