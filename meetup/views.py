from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from meetup.models import Talk
from models import Event


class IndexPage(ListView):
    template_name = 'index.html'
    context_object_name = 'events'
    queryset = Event.archived.all().prefetch_related('talks', 'talks__speaker')

    def get_active_event(self):
        try:
            next_event = Event.active.all().prefetch_related('talks', 'talks__speaker').latest()
        except Event.DoesNotExist:
            next_event = None
        return next_event

    def get_context_data(self, **kwargs):
        context = super(IndexPage, self).get_context_data(**kwargs)

        context.update({
            'next_event': self.get_active_event(),
            'with_dash': self.request.GET.get('with_dash', False)
        })
        return context


class EventPage(DetailView):
    template_name = 'event.html'
    model = Event


class TalkPage(DetailView):
    template_name = 'talk.html'
    model = Talk
