from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from meetup.models import Talk
from models import Event


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
    queryset = Event.visible.all()


class TalkPage(DetailView):
    template_name = 'talk.html'
    slug_url_kwarg = 'talk_slug'

    def get_queryset(self):
        return Talk.active.filter(event_id=self.kwargs['event_id'])


class AboutPage(TemplateView):
    template_name = 'about.html'


class LivePage(TemplateView):
    template_name = 'live.html'

    def get_context_data(self, **kwargs):
        context = super(LivePage, self).get_context_data(**kwargs)

        context.update({
            'event': Event.objects.upcoming(),
        })
        return context
