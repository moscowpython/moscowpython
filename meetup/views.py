from django.views.generic.list import ListView
from models import Event


class IndexPage(ListView):
    template_name = 'index.html'
    context_object_name = 'events'
    queryset = Event.archived.all()

    def get_context_data(self, **kwargs):
        context = super(IndexPage, self).get_context_data(**kwargs)
        try:
            next_event = Event.active.latest()
        except Event.DoesNotExist:
            next_event = None
        context.update({
            'next_event': next_event
        })
        return context