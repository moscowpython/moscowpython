# -*- coding: utf-8 -*-
from django.db import models


class Talk(models.Model):
    name = models.CharField(u'Название', max_length=1024)
    company_name = models.CharField(u'Название компании', max_length=1024)
    speaker = models.ForeignKey('Speaker', related_name='talks')
    event = models.ForeignKey('Event', related_name='talks')
    description = models.TextField(u'Описание', blank=True)
    presentation = models.URLField(u'Адрес презентации', blank=True)
    video = models.URLField(u'Адрес видео', blank=True)

    class Meta:
        verbose_name = u'Выступление'
        verbose_name_plural = u'Выступление'


class Event(models.Model):
    name = models.CharField(u'Название', max_length=1024)
    description = models.TextField(u'Описание', blank=True)
    image = models.ImageField(u'Изображение', upload_to='events', null=True, blank=True)
    date = models.DateTimeField(u'Начало', blank=True, null=True)
    address = models.TextField(u'Место проведения', blank=True)
    sponsors = models.ManyToManyField('Sponsor', blank=True)

    class Meta:
        verbose_name = u'Событие'
        verbose_name_plural = u'События'


class Speaker(models.Model):
    name = models.CharField(u'Имя', max_length=100)
    photo = models.ImageField(u'Фотография', upload_to='speakers', null=True, blank=True)

    class Meta:
        verbose_name = u'Докладчик'
        verbose_name_plural = u'Докладчики'


class Sponsor(models.Model):
    name = models.CharField(u'Название компании')
    logo = models.ImageField(u'Логотип', upload_to='sponsors')

    class Meta:
        verbose_name = u'Спонсор'
        verbose_name_plural = u'Спонсоры'
