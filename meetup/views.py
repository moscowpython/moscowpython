from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Talk, Photo, Speaker, Event, Tutorial
from .utils import subscribe_mail, validate_email


class IndexPage(ListView):
    template_name = 'index.html'
    context_object_name = 'events'
    queryset = Event.archived.all().prefetch_related('talks', 'talks__speaker')

    def get_last_event(self):
        try:
            active_event = Event.visible.all().prefetch_related('talks', 'talks__speaker').latest()
        except Event.DoesNotExist:
            active_event = None
        return active_event

    def get_context_data(self, **kwargs):
        context = super(IndexPage, self).get_context_data(**kwargs)

        context.update({
            'main_event': self.get_last_event(),
        })
        return context


class EventsList(ListView):
    template_name = 'event_list.html'
    queryset = Event.visible.all()
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
    queryset = Talk.active.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
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
    model = Speaker


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


class TutorialList(ListView):
    template_name = 'tutorials.html'
    queryset = Tutorial.objects.all().order_by('title')
    context_object_name = 'tutorials'


class TutorialPage(DetailView):
    template_name = 'tutorial.html'
    model = Tutorial

def ajax_subscribe(request):
    if "email" in request.POST:
        email = request.POST['email']
        if validate_email(email) and subscribe_mail(email):
            return HttpResponse('OK')
    return HttpResponse('Failed')

