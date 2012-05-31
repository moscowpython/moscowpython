from django.views.generic.list import ListView
from models import Event


class IndexPage(ListView):
    template_name = 'index.html'
    context_object_name = 'events'
    model = Event

    def get_context_data(self, **kwargs):
        context = super(IndexPage, self).get_context_data(**kwargs)
        context.update({
            'next_event': Event.objects.latest()
        })
        return context