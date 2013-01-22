# -*- coding: utf-8 -*-
from django.db import models
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel


class Vacancy(StatusModel, TimeStampedModel):
    STATUS = Choices('active', 'draft')
    TYPE = Choices(('fulltime', u'Фултайм'), ('contract', u'Контракт'))

    company = models.CharField(u'Компания', max_length=100)
    name = models.CharField(u'Должность', max_length=100)
    description = models.TextField(u'Текст', help_text=u'Markdown', blank=True)
    contacts = models.TextField(u'Контакты', help_text=u'Markdown', blank=True)
    type = models.CharField(u'Занятость', choices=TYPE, default='fulltime', max_length=50)
    is_participant = models.BooleanField(u'На митапе', default=False)
    is_priority = models.BooleanField(u'Приоритетная вакансия', default=False)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'vacancy', [self.pk]

    class Meta:
        verbose_name = u'Вакансия'
        verbose_name_plural = u'Вакансии'
        ordering = ['-is_priority', '-modified']