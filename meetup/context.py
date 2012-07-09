# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from models import Event


def menu(request):
    menu_items = (
        {'title':u'События', 'url':'events'},
        {'title':u'Группа на Фейсбуке', 'url':'http://www.facebook.com/groups/MoscowDjango/'},
        {'title':u'О проекте', 'url':None},
    )

    for item in menu_items:
        if item['url'] is not None:
            if not item['url'].startswith('http'):
                item['url'] = reverse_lazy(item['url'])

    return {'menu_items': menu_items}


def all_events_processor(request):
    return {
        'all_events': Event.visible.all()
    }
