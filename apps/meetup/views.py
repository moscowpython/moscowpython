# coding=utf-8
import os
import sys

import django
from django.core.urlresolvers import reverse
from django.db import DatabaseError
from django.db.models import Count
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.utils import six
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt

from .models import Talk, Photo, Speaker, Event, Tutorial, Vote
from .utils import subscribe_mail, validate_email, set_vote_cookie, can_vote


class IndexPage(ListView):
    template_name = 'index.html'
    context_object_name = 'events'

    def get_queryset(self):
        if self.request.user.is_staff:
            qs = Event.objects.all()
        else:
            qs = Event.archived.all()

        return qs.prefetch_related('talks', 'talks__speaker', 'talks__event')[:3]

    def get_context_data(self, **kwargs):
        context = super(IndexPage, self).get_context_data(**kwargs)

        # TODO: choose how select people for index page
        # I see two options:
        # By last talks -  Speaker.objects.order_by("-talks__event__id", "talk__position")[:9]
        # Random: Speaker.objects.order_by("?")[:9]

        context.update({
            'speakers': Speaker.objects.order_by("?")[:10],
            'main_event': Event.spotlight(self.request.user.is_staff),
            'show_more_link': True,
            'can_vote': can_vote(self.request)
        })
        return context


class EventsList(ListView):
    template_name = 'event_list.html'
    queryset = Event.visible.prefetch_related('talks', 'talks__speaker', 'talks__event')
    context_object_name = 'events'

    def get_queryset(self):
        if self.request.user.is_staff:
            qs = Event.objects.all()
        else:
            qs = Event.visible.all()
        return qs.prefetch_related('talks', 'talks__speaker', 'talks__event')


class EventPage(DetailView):
    template_name = 'event.html'
    slug_url_kwarg = 'number'
    slug_field = 'number'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Event.objects.all()
        return Event.visible.all()

    def get_context_data(self, **kwargs):
        context = super(EventPage, self).get_context_data(**kwargs)
        context.update({
            'photos': context['event'].photos.all(),
            'can_vote': can_vote(self.request),
        })
        return context


class TalkPage(DetailView):
    template_name = 'talk.html'
    slug_url_kwarg = 'talk_slug'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Talk.objects.select_related('event', 'speaker')
        return Talk.objects.active().select_related('event', 'speaker')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Redirect for non-canonic urls (meetup.legacy.urls)
        if self.object.get_absolute_url() != request.path:
            return redirect(self.object)

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class SpeakerList(ListView):
    template_name = 'speakers.html'
    queryset = Speaker.objects.all().order_by('name')
    context_object_name = 'speakers'


class SpeakerPage(DetailView):
    template_name = 'speaker.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Speaker.objects.prefetch_related('talks', 'talks__event'),
            slug=self.kwargs['slug']
        )


class AboutPage(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutPage, self).get_context_data(**kwargs)
        context.update({
            'photos': Photo.objects.all().order_by('-pk')[:10]
        })
        return context


class LivePage(TemplateView):
    template_name = 'live.html'

    def get_context_data(self, **kwargs):
        context = super(LivePage, self).get_context_data(**kwargs)

        context.update({
            'event': Event.spotlight(),
        })
        return context


class TutorialList(ListView):
    template_name = 'tutorials.html'
    queryset = Tutorial.objects.all().order_by('title')
    context_object_name = 'tutorials'


class TutorialPage(DetailView):
    template_name = 'tutorial.html'
    model = Tutorial


class Py3Page(TemplateView):
    template_name = 'py3.html'

    def get_context_data(self, **kwargs):
        context = super(Py3Page, self).get_context_data(**kwargs)

        context.update({
            'django': django.get_version(),
            'python': sys.version,
            'py3': six.PY3,
        })
        return context


class VoteResults(TemplateView):
    template_name = 'vote_results.html'

    def get_context_data(self, **kwargs):
        context = super(VoteResults, self).get_context_data(**kwargs)
        talks = Talk.objects.filter(event=Event.spotlight()).annotate(num_votes=Count("votes"))

        talks_votes = [talk.num_votes for talk in talks]
        votes_total = sum(talks_votes)
        votes_max = max(talks_votes)
        if votes_total:
            for talk in talks:
                talk.votes_percent = int(talk.num_votes * 100 / votes_total)
                if talk.num_votes == votes_max:
                    talk.is_leader = True
        context.update({
            'talks': talks,
        })

        return context


@csrf_exempt
def ajax_vote(request, *args, **kwargs):
    if request.method == 'POST':
        if not can_vote(request):
            return HttpResponse(u'Можно голосовать только за один доклад', status=409)
        try:
            event = Talk.objects.get(pk=kwargs['talk_id']).event
            if not event.votable:
                return HttpResponse('Voting is closed, sorry', status=409)
            Vote.objects.create(talk_id=kwargs['talk_id'],
                                event=event,
                                ua=request.META.get('HTTP_USER_AGENT'),
                                ip=request.META.get('REMOTE_ADDR'))
            response = HttpResponse(reverse('vote-results'))
            response = set_vote_cookie(response)
            return response
        except DatabaseError:
            return HttpResponse('DB error, sorry', status=402)
    return HttpResponse('Only POST', status=402)


def confirm_ownership(request, *args, **kwargs):
    content = os.environ.get('CONFIRM_OWNERSHIP_%s' % kwargs['filename'], None)
    if content:
        content_type = 'text/html' if kwargs['filename'].endswith('.html') else 'text/plain'
        return HttpResponse(content, content_type=content_type)
    else:
        raise Http404
