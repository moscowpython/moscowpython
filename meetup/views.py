import django
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils import six
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
import sys
from .models import Talk, Photo, Speaker, Event
from .utils import subscribe_mail, validate_email


class IndexPage(ListView):
    template_name = 'index.html'
    context_object_name = 'events'
    queryset = Event.archived.prefetch_related('talks', 'talks__speaker', 'talks__event')

    def get_context_data(self, **kwargs):
        context = super(IndexPage, self).get_context_data(**kwargs)

        context.update({
            'main_event': Event.objects.upcoming(),
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
            'photos': context['event'].photos.all()
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
            'event': Event.objects.upcoming(),
        })
        return context


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


def ajax_subscribe(request):
    if "email" in request.POST:
        email = request.POST['email']
        if validate_email(email) and subscribe_mail(email):
            return HttpResponse('OK')
    return HttpResponse('Failed')
