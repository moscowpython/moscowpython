# coding: utf-8
import urllib
from celery import shared_task
from apps.vacancies.parsers import VacancySync, YandexRabotaParser


@shared_task
def update_vacancies():
    fulltime = {
        'rid': 213,
        'currency': 'RUR',
        'text': 'python программист',
        'strict': 'false',
        'employment': 'FULL_EMPLOYMENT'
    }
    part_time = fulltime.copy()
    part_time['employment'] = 'TEMPORARY_EMPLOYMENT'

    syncer = VacancySync(parsers=[
        YandexRabotaParser(urllib.parse.urlencode(fulltime), type='fulltime'),
        YandexRabotaParser(urllib.parse.urlencode(part_time), type='contract')
    ])
    syncer.sync()
