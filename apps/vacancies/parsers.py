# coding: utf-8
import re

import arrow
from arrow.locales import RussianLocale, EnglishLocale
from dateutil.tz import tzoffset
from django.utils.timezone import make_naive
import requests
import xmltodict

from apps.vacancies.models import Vacancy


class VacancySync:

    def __init__(self, parsers=None):
        self.parsers = parsers or [YandexRabotaParser()]

    def sync(self):
        for parser in self.parsers:
            for vacancy_dict in parser.get_vacancies():
                vacancy_dict['published_at'] = make_naive(vacancy_dict['published_at'], tzoffset(None, 14400))

                # TODO: replace with https://docs.djangoproject.com/en/dev/ref/models/querysets/#update-or-create
                try:
                    obj = Vacancy.objects.get(url=vacancy_dict['url'])
                    for key, value in vacancy_dict.items():
                        setattr(obj, key, value)
                    obj.save()
                except Vacancy.DoesNotExist:
                    Vacancy.objects.create(**vacancy_dict)


class YandexRabotaParser:

    def __init__(self, querystring='', **kwargs):
        self.url = 'http://rabota.yandex.ru/rss.xml?' + querystring
        self.kwargs = kwargs or {}

    @staticmethod
    def parse_date(string):
        """ Parse localized date from Yandex.Rabota XML feed

            Because month name is localized we can't properly parse it
            without depending on setlocale, with is env-dependent.
            month_abbreviations are generated from calendar module, which relies on %B
        """
        replacement_mapping = dict(zip(RussianLocale().month_abbreviations, EnglishLocale().month_abbreviations))
        for rus, eng in replacement_mapping.items():
            string = re.compile(rus, re.I).sub(eng, string)

        return arrow.get(string, 'DD MMM YYYY HH:mm:ss Z').datetime

    @staticmethod
    def extract_title(title):
        title_match = re.match('(?P<position>.+?)\((?P<salary>.+?)\)', title)
        if title_match:
            name = title_match.group('position')
            salary = title_match.group('salary')
        else:
            name = title
            salary = ''
        return name, salary

    @staticmethod
    def extract_desc(desc):
        desc_match = re.match('^Вакансия от \w+ (?P<company>.+)\.<br/>(?P<desc>.+)$', desc, re.S)
        if desc_match:
            company = desc_match.group('company')
            description = desc_match.group('desc')
        else:
            company = 'Неизвестная'
            description = desc
        return description, company

    def get_vacancies(self):
        response = requests.get(self.url)

        if response.status_code != requests.codes.ok:
            raise Exception('Web request failed, %s' % response.text)

        data = xmltodict.parse(response.text)
        vacancies = data['rss']['channel']['item']
        if not isinstance(vacancies, list):
            vacancies = [vacancies]
        for vacancy in vacancies:
            name, salary = self.extract_title(vacancy['title'])
            description, company = self.extract_desc(vacancy['description'])
            yield dict({
                'name': name.strip(),
                'company': company,
                'salary': salary,
                'url': vacancy['link'],
                'published_at': self.parse_date(vacancy['pubDate']),
                'description': description,
            }, **self.kwargs)
