# coding=utf-8
import os

from django.http import HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Talk, Photo, Speaker, Event, Tutorial
from .utils import can_vote


class IndexPage(ListView):
    template_name = 'index.html'
    context_object_name = 'events'
    queryset = Event.archived.prefetch_related('talks', 'talks__speaker', 'talks__event')[:3]

    def get_context_data(self, **kwargs):
        context = super(IndexPage, self).get_context_data(**kwargs)

        # TODO: choose how select people for index page
        # I see two options:
        # By last talks -  Speaker.objects.order_by("-talks__event__id", "talk__position")[:9]
        # Random: Speaker.objects.order_by("?")[:9]

        context.update({
            'speakers': Speaker.objects.order_by("?")[:10],
            'main_event': Event.spotlight(),
            'show_more_link': True,
            'can_vote': can_vote(self.request)
        })
        return context


class EventsList(ListView):
    template_name = 'event_list.html'
    queryset = Event.visible.prefetch_related('talks', 'talks__speaker', 'talks__event')
    context_object_name = 'events'


class EventPage(DetailView):
    template_name = 'event.html'
    slug_url_kwarg = 'number'
    slug_field = 'number'
    queryset = Event.visible.all()

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
    queryset = Talk.active.select_related('event', 'speaker')

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


def confirm_ownership(request, *args, **kwargs):
    content = os.environ.get('CONFIRM_OWNERSHIP_%s' % kwargs['filename'], None)
    if content:
        content_type = 'text/html' if kwargs['filename'].endswith('.html') else 'text/plain'
        return HttpResponse(content, content_type=content_type)
    else:
        raise Http404
