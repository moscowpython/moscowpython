from __future__ import annotations

from django import forms
from django.forms import ModelForm

from .models import Event, Sponsor


class EventAdminForm(ModelForm):
    sponsors = forms.ModelMultipleChoiceField(queryset=Sponsor.objects.all(), widget=forms.CheckboxSelectMultiple())

    def __init__(self, *args, **kwargs):
        super(EventAdminForm, self).__init__(*args, **kwargs)
        self.fields['manual_on_air'].widget.choices = (('1', 'Автоматически'), ('2', 'Вкл'), ('3', 'Выкл'))

    class Meta:
        model = Event
        exclude = []  # This is admin form FFS
