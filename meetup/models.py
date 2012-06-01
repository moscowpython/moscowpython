# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import permalink
from model_utils import Choices
from model_utils.models import StatusModel


class Talk(models.Model):
    name = models.CharField(u'Название', max_length=1024)
    speaker = models.ForeignKey('Speaker', verbose_name=u'Докладчик', related_name='talks')
    event = models.ForeignKey('Event', verbose_name=u'Событие', related_name='talks')
    description = models.TextField(u'Описание', blank=True)
    presentation = models.URLField(u'Адрес презентации', blank=True)
    video = models.URLField(u'Адрес видео', blank=True)

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return 'talk', [self.pk]

    class Meta:
        verbose_name = u'Выступление'
        verbose_name_plural = u'Выступление'


class Event(StatusModel):
    STATUS = Choices('draft', 'active', 'archived')

    name = models.CharField(u'Название', max_length=1024)
    description = models.TextField(u'Описание', blank=True)
    image = models.ImageField(u'Изображение', upload_to='events', null=True, blank=True)
    date = models.DateTimeField(u'Начало', blank=True, null=True)
    address = models.TextField(u'Место проведения', blank=True)
    latitude = models.DecimalField(u'Широта', decimal_places=6, max_digits=9, blank=True, null=True)
    longitude = models.DecimalField(u'Долгота', decimal_places=6, max_digits=9, blank=True, null=True)
    sponsors = models.ManyToManyField('Sponsor', verbose_name=u'Спонсоры', blank=True)

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return 'event', [self.pk]

    class Meta:
        verbose_name = u'Событие'
        verbose_name_plural = u'События'
        get_latest_by = 'id'
        ordering = ['-date']


class Speaker(models.Model):
    name = models.CharField(u'Имя', max_length=100)
    photo = models.ImageField(u'Фотография', upload_to='speakers', null=True, blank=True)
    company_name = models.CharField(u'Название компании', max_length=1024, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Докладчик'
        verbose_name_plural = u'Докладчики'


class Sponsor(models.Model):
    name = models.CharField(u'Название компании', max_length=250)
    logo = models.ImageField(u'Логотип', upload_to='sponsors')
    url = models.URLField(u'Адрес сайта', blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Спонсор'
        verbose_name_plural = u'Спонсоры'
