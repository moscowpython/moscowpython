# -*- coding: utf-8 -*-
from django.forms import ModelForm
from .models import Event


class EventAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(EventAdminForm, self).__init__(*args, **kwargs)
        self.fields['manual_on_air'].widget.choices = \
            ((u'1', 'Автоматически'),
             (u'2', 'Вкл'),
             (u'3', 'Выкл'))

    class Meta:
        model = Event