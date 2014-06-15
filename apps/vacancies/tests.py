# coding: utf-8
import datetime
from pathlib import Path

from dateutil.tz import tzoffset
from django.core.urlresolvers import reverse
from django.test import TestCase
import httpretty
from django.conf import settings

from apps.vacancies.models import Vacancy
from apps.vacancies.parsers import YandexRabotaParser


class VacancyList(TestCase):
    """Integration tests for vacancy list page"""

    def test_vacancies(self):
        vacancy1 = Vacancy.objects.create(name='XXX', company='a', url='http://yandex.ru')
        vacancy2 = Vacancy.objects.create(name='YYY', company='b', url='http://mail.ru')
        response = self.client.get(reverse('vacancies'))
        self.assertQuerysetEqual(response.context['vacancies'], list(map(repr, [vacancy2, vacancy1])))


class VacancyDetail(TestCase):
    """Integration tests for vacancy detail page"""

    def test_vacancy(self):
        vacancy = Vacancy.objects.create(name='Vacancy1', company='slug')
        response = self.client.get(reverse('vacancy', args=[1]))
        self.assertEqual(response.context['vacancy'], vacancy)


class ParserTest(TestCase):

    def test_parse_date(self):
        assert YandexRabotaParser.parse_date('Cбт, 14 Июн 2014 18:03:11 +0400') == \
               datetime.datetime(2014, 6, 14, 18, 3, 11, tzinfo=tzoffset(None, 14400))
        assert YandexRabotaParser.parse_date('Cб., 14 июня 2014 08:44:36 +0400') == \
               datetime.datetime(2014, 6, 14, 8, 44, 36, tzinfo=tzoffset(None, 14400))

    def test_extract_desc(self):
        assert YandexRabotaParser.extract_desc('Вакансия от компании Платформа Alytics.<br/>Что мы используем: - Python 2.7,pip') == \
               ('Что мы используем: - Python 2.7,pip', 'Платформа Alytics')
        assert YandexRabotaParser.extract_desc('Вакансия от агентства Дижитал-Персонал-Сервис.<br/>Воу, бро!') == \
               ('Воу, бро!', 'Дижитал-Персонал-Сервис')

    @httpretty.activate
    def test_get_vacancies(self):
        xml_content = open(str(Path(settings.ROOT_PATH) / 'apps' / 'vacancies' / 'data' / 'rabota.xml')).read()
        httpretty.register_uri(httpretty.GET, "http://rabota.yandex.ru/rss.xml",
                               body=xml_content)

        self.assertEqual(list(YandexRabotaParser().get_vacancies())[:2], [
            {
                'name': 'Python / PHP программист',
                'salary': 'от 100 000 до 160 000 руб.',
                'company': 'РосБизнесКонсалтинг',
                'url': 'http://www.superjob.ru/rabota/vacancy-26574727-140611.html',
                'published_at': datetime.datetime(2014, 6, 15, 13, 50, 26, tzinfo=tzoffset(None, 14400)),
                'description': 'опыт программирования'
                               ' на языке Python/PHP от 3 лет; - Linux (nix) на уровне пользователя,'
                               ' желание получить навыки администрирования; - опыт работы с какой-либо'
                               ' реляционной СУБД, базовый уровень знаний в SQL; - умение читать и понимать чужой код;'
                               ' - понимание HTML/XML, JavaScript, DOM.'
                               '\nразработка и поддержка высоконагруженных интернет-проектов (несколько миллионов'
                               ' просмотров в сутки), интернет-...'
            }, {
                'name': 'Ведущий программист Python / Perl',
                'salary': '',
                'company': 'РосБизнесКонсалтинг',
                'url': 'http://www.superjob.ru/rabota/vacancy-26575242-140611.html',
                'published_at': datetime.datetime(2014, 6, 15, 13, 50, 26, tzinfo=tzoffset(None, 14400)),
                'description': 'разработка и поддержка '
                               'высоконагруженных интернет-проектов (несколько миллионов просмотров в сутки), '
                               'интернет-сервисов на языке Python/Perl; - разработка и поддержка внутренних '
                               'вспомогательных систем.\nконкурентоспособная,"белая" заработная плата, обсуждается '
                               'с успешным кандидатом после технического интервью. - молодой и дружный коллектив, '
                               'возможность расти и развиваться в компании с...'
            }
        ])
