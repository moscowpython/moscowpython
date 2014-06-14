# coding: utf-8
from django.core.urlresolvers import reverse
from django.test import TestCase
from apps.vacancies.models import Vacancy


class VacancyList(TestCase):
    """Integration tests for vacancy list page"""

    def test_vacancies(self):
        vacancy1 = Vacancy.objects.create(name='XXX', company='a')
        vacancy2 = Vacancy.objects.create(name='YYY', company='b')
        response = self.client.get(reverse('vacancies'))
        self.assertQuerysetEqual(response.context['vacancies'], list(map(repr, [vacancy2, vacancy1])))


class VacancyDetail(TestCase):
    """Integration tests for vacancy detail page"""

    def test_vacancy(self):
        vacancy = Vacancy.objects.create(name='Vacancy1', company='slug')
        response = self.client.get(reverse('vacancy', args=[1]))
        self.assertEqual(response.context['vacancy'], vacancy)
