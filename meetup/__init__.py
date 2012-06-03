from models import Event


def all_events_processor(request):
    return {
        'all_events': Event.visible.all()
    }