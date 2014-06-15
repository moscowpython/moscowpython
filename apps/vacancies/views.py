# coding: utf-8
from django.views.generic import ListView, DetailView
from .models import Vacancy


class VacancyList(ListView):
    template_name = 'vacancies.html'
    queryset = Vacancy.active.all()
    context_object_name = 'vacancies'


class VacancyPage(DetailView):
    template_name = 'vacancy.html'
    model = Vacancy

    def get_context_data(self, **kwargs):
        data = super(VacancyPage, self).get_context_data(**kwargs)
        data['vacancy_count'] = Vacancy.active.count()
        return data

