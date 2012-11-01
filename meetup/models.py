# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.db.models import permalink
from embedly.client import Embedly
from django.db.models.manager import Manager
from model_utils import Choices
from model_utils.managers import QueryManager, PassThroughManager
from model_utils.models import StatusModel
from picklefield.fields import PickledObjectField

class TalkManager(Manager):

    def active(self):
        qs = self.get_query_set()
        return qs.filter(status="active")

class Talk(StatusModel):
    STATUS = Choices('draft', 'active')

    name = models.CharField(u'Название', max_length=1024)
    speaker = models.ForeignKey('Speaker', verbose_name=u'Докладчик', related_name='talks')
    event = models.ForeignKey('Event', verbose_name=u'Событие', related_name='talks')
    slug = models.SlugField(u'Код')
    description = models.TextField(u'Описание', blank=True)
    presentation = models.URLField(u'Адрес презентации', blank=True)
    presentation_data = PickledObjectField(u'Meta-данные презентации', editable=True, blank=True)
    video = models.URLField(u'Адрес видео', blank=True)
    video_data = PickledObjectField(u'Meta-данные видео', blank=True)
    position = models.SmallIntegerField(u'Порядок выступления на событии', default=0)

    objects = TalkManager()

    original_presentation = None
    original_video = None

    def __init__(self, *args, **kwargs):
        super(Talk, self).__init__(*args, **kwargs)
        self.original_presentation = self.presentation
        self.original_video = self.video

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return 'talk', [self.event.number, self.slug]

    def set_embedly_data(self, field_name):
        original_field_value = getattr(self, 'original_{0}'.format(field_name))
        new_field_value = getattr(self, field_name)
        if new_field_value != original_field_value:
            embedly_key = getattr(settings, 'EMBEDLY_KEY')
            if embedly_key:
                client = Embedly(embedly_key)
                data_field_name = '{0}_data'.format(field_name)
                setattr(self, data_field_name, client.oembed(new_field_value).data)
        setattr(self, 'original_{0}'.format(field_name), new_field_value)

    def save(self, *args, **kwargs):
        self.set_embedly_data('presentation')
        self.set_embedly_data('video')
        super(Talk, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'Выступление'
        verbose_name_plural = u'Выступления'
        ordering = ('position',)


class EventQuerySet(models.query.QuerySet):
    def upcoming(self):
        try:
            return self.filter(status=Event.STATUS.active).latest()
        except Event.DoesNotExist:
            return None


class Event(StatusModel):
    STATUS = Choices('draft', 'planning', 'active', 'archived')

    name = models.CharField(u'Название', max_length=1024)
    number = models.SmallIntegerField(u'Номер', blank=True, null=True)
    description = models.TextField(u'Описание', blank=True)
    image = models.ImageField(u'Изображение', upload_to='events', null=True, blank=True)
    date = models.DateTimeField(u'Начало', blank=True, null=True)
    venue = models.ForeignKey('Venue', blank=True, null=True)
    sponsors = models.ManyToManyField('Sponsor', verbose_name=u'Спонсоры', blank=True)
    timepad_id = models.IntegerField(u'ID события на Timepad', blank=True, default=0)

    objects = PassThroughManager.for_queryset_class(EventQuerySet)()
    visible = QueryManager(status__in=[STATUS.planning, STATUS.active, STATUS.archived])

    def __unicode__(self):
        if self.number:
            return u'{0} №{1}'.format(self.name, self.number)
        else:
            return self.name

    @permalink
    def get_absolute_url(self):
        return 'event', [self.number]

    @property
    def is_active(self):
        return self.status == self.STATUS.active

    def get_timepad_url(self):
        if self.timepad_id:
            return 'http://moscowdjango.timepad.ru/event/%s/' % self.timepad_id

    class Meta:
        verbose_name = u'Событие'
        verbose_name_plural = u'События'
        get_latest_by = 'id'
        ordering = ['-date']


class Venue(models.Model):
    name = models.CharField(u'Название места', max_length=100)
    address = models.TextField(u'Адрес')
    latitude = models.DecimalField(u'Широта', decimal_places=6, max_digits=9, blank=True, null=True)
    longitude = models.DecimalField(u'Долгота', decimal_places=6, max_digits=9, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Место'
        verbose_name_plural = u'Места'


class Speaker(models.Model):
    name = models.CharField(u'Имя', max_length=100)
    photo = models.ImageField(u'Фотография', upload_to='speakers', null=True, blank=True)
    company_name = models.CharField(u'Название компании', max_length=1024, blank=True)

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return 'speaker', [self.pk]

    @property
    def avatar_url(self):
        if self.photo:
            return self.photo.url
        else:
            return settings.STATIC_URL + 'images/avatars/reinhardt.png'

    class Meta:
        verbose_name = u'Докладчик'
        verbose_name_plural = u'Докладчики'


class Photo(models.Model):
    event = models.ForeignKey(Event, related_name='photos', blank=True, null=True)
    url = models.URLField(u'Ссылка на внешнее фото', help_text=u'Временное поле', blank=True)
    image = models.ImageField(u'Фотография', upload_to='photos', blank=True)
    caption = models.TextField(u'Подпись', blank=True)

    def __unicode__(self):
        return self.caption or u'Фото №%s' % self.id

    def get_absolute_url(self):
        if self.url:
            return self.url
        else:
            return self.image.url

    class Meta:
        verbose_name = u'Фотография'
        verbose_name_plural = u'Фотографии'


class Sponsor(models.Model):
    name = models.CharField(u'Название компании', max_length=250)
    logo = models.ImageField(u'Логотип', upload_to='sponsors')
    url = models.URLField(u'Адрес сайта', blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.url

    class Meta:
        verbose_name = u'Спонсор'
        verbose_name_plural = u'Спонсоры'


class MediaCoverage(models.Model):
    event = models.ForeignKey(Event, related_name='media_coverages')
    name = models.CharField(u'Название упоминания', max_length=250)
    url = models.URLField(u'Адрес страницы с упоминанием')
    ico = models.CharField(u'Ссылка на .ico сайта', max_length=250, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.url

    class Meta:
        verbose_name = u'Упоминание'
        verbose_name_plural = u'Упоминания'
