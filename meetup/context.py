# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from models import Event


def menu(request):
    menu_items = (
        {'title':u'События', 'url':'events'},
        {'title':u'Видео', 'url':'http://www.youtube.com/moscowdjangoru'},
        {'title':u'Группа Facebook', 'url':'http://www.facebook.com/groups/MoscowDjango/'},
        {'title':u'Люди', 'url':'speakers'},
        {'title':u'О проекте', 'url':'about'},
    )

    for item in menu_items:
        if item['url'] is not None:
            if item['url'].startswith('http'):
                item['external'] = True
            else:
                item['external'] = False
                item['url'] = reverse_lazy(item['url'])

    return {'menu_items': menu_items}


def all_events_processor(request):
    return {
        'all_events': Event.visible.all()
    }
