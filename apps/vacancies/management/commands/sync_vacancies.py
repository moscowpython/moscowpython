# coding: utf-8
from django.core.management.base import BaseCommand

from apps.vacancies.tasks import update_vacancies


class Command(BaseCommand):
    help = 'Updates vacancies'

    def handle(self, *args, **options):
        result = update_vacancies()
        self.stdout.write('Created vacancies: %s' % result['created_count'])
        self.stdout.write('Updated vacancies: %s' % result['updated_count'])
