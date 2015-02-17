# coding: utf-8
import datetime

from django.conf import settings
from django.db import models
from django.db.models import permalink
from embedly.client import Embedly
from django.db.models.manager import Manager
from model_utils import Choices
from model_utils.managers import QueryManager
from model_utils.models import StatusModel, TimeStampedModel
from picklefield.fields import PickledObjectField


class TalkManager(Manager):
    def active(self):
        qs = self.get_query_set()
        return qs.filter(status="active")


class Talk(StatusModel):
    STATUS = Choices('active', 'draft')

    name = models.CharField(u'Название', max_length=1024)
    speaker = models.ForeignKey('Speaker', verbose_name=u'Докладчик', related_name='talks')
    event = models.ForeignKey('Event', verbose_name=u'Событие', related_name='talks')
    slug = models.SlugField(u'Код')
    description = models.TextField(u'Описание', blank=True)
    presentation = models.URLField(u'Адрес презентации', blank=True)
    presentation_data = PickledObjectField(u'Meta-данные презентации', editable=True, blank=True)
    video = models.URLField(u'Адрес видео', blank=True)
    video_data = PickledObjectField(u'Meta-данные видео', blank=True)
    position = models.SmallIntegerField(u'Порядок', help_text=u'Порядок выступления на событии', default=0)

    objects = TalkManager()

    original_presentation = None
    original_video = None

    def __init__(self, *args, **kwargs):
        super(Talk, self).__init__(*args, **kwargs)
        self.original_presentation = self.presentation
        self.original_video = self.video

    def __str__(self):
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
                setattr(self, data_field_name, client.oembed(new_field_value)._data)
        setattr(self, 'original_{0}'.format(field_name), new_field_value)

    def save(self, *args, **kwargs):
        self.set_embedly_data('presentation')
        self.set_embedly_data('video')
        super(Talk, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'Выступление'
        verbose_name_plural = u'Выступления'
        ordering = ('-event__number', 'position',)


class Event(StatusModel):
    """ Events
        * draft - totally invisible
        * planning - only event description is shown
        * active - event is scheduled, speakers also visible
        * archived - event passed, registration is disabled
    """
    STATUS = Choices('planning', 'active', 'archived', 'draft',)

    name = models.CharField(u'Название', max_length=1024)
    number = models.SmallIntegerField(u'Номер', blank=True, null=True)
    description = models.TextField(u'Описание', blank=True)
    image = models.ImageField(u'Изображение', upload_to='events', null=True, blank=True)
    date = models.DateTimeField(u'Начало', blank=True, null=True)
    venue = models.ForeignKey('Venue', blank=True, null=True)
    sponsors = models.ManyToManyField('Sponsor', verbose_name=u'Спонсоры', blank=True)
    timepad_id = models.IntegerField(u'ID события на Timepad', blank=True, default=0)
    registration_link = models.URLField(u'Ссылка на событие', blank=True)
    streaming_url = models.URLField(u'Ссылка на трансляцию', blank=True)
    manual_on_air = models.NullBooleanField(u'Включить трансляцию', default=None,
                                            help_text=u'Включается автоматически за полчаса до начала и идёт 4 часа.'
                                                      u' Нужно, для тестирования в другое время.')
    votable = models.BooleanField(u'Включить голосование', default=False)

    objects = Manager()
    visible = QueryManager(status__in=[STATUS.planning, STATUS.active, STATUS.archived])

    def __str__(self):
        if self.number:
            return u'{0} №{1}'.format(self.name, self.number)
        else:
            return self.name

    def __repr__(self):
        return '<Event №%s>' % self.number

    @permalink
    def get_absolute_url(self):
        return 'event', [self.number]

    @property
    def is_active(self):
        return self.status == self.STATUS.active

    def days_delta(self):
        if not self.date:
            return None
        delta = (self.date.date() - datetime.datetime.today().date()).days
        if delta < 0:
            return None  # passed
        if delta >= 0:
            return delta

    @property
    def on_air(self):
        if self.manual_on_air is not None:
            return self.manual_on_air
        datetime_start = self.date - datetime.timedelta(minutes=30)
        datetime_stop = self.date + datetime.timedelta(hours=4)  # Actually meetups are not that long
        return datetime_start <= datetime.datetime.now() <= datetime_stop

    def get_registration_url(self):
        if self.timepad_id:
            return 'https://moscowdjango.timepad.ru/event/%s/' % self.timepad_id
        if self.registration_link:
            return self.registration_link

    @classmethod
    def spotlight(cls):
        """ Last active or last planned or last archived
        """
        try:
            return Event.visible.latest()
        except Event.DoesNotExist:
            return None

    class Meta:
        verbose_name = u'Событие'
        verbose_name_plural = u'События'
        get_latest_by = 'number'
        ordering = ['-date']


class Venue(models.Model):
    name = models.CharField(u'Название места', max_length=100)
    address = models.TextField(u'Адрес')
    latitude = models.DecimalField(u'Широта', decimal_places=6, max_digits=9, blank=True, null=True)
    longitude = models.DecimalField(u'Долгота', decimal_places=6, max_digits=9, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Место'
        verbose_name_plural = u'Места'


class Speaker(models.Model):
    name = models.CharField(u'Имя', max_length=100)
    slug = models.SlugField(u'Слаг', default='')
    photo = models.ImageField(u'Фотография', upload_to='speakers', null=True, blank=True)
    company_name = models.CharField(u'Название компании', max_length=1024, blank=True)
    description = models.TextField(u'Описание', blank=True)

    def __str__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return 'speaker', [self.slug]

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

    def __str__(self):
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
    STATUSES = Choices('organizer', 'partner')

    name = models.CharField(u'Название компании', max_length=250)
    logo = models.ImageField(u'Логотип', upload_to='sponsors')
    url = models.URLField(u'Адрес сайта', blank=True)
    status = models.CharField(u'Тип', choices=STATUSES, max_length=10)

    def __str__(self):
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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.url

    class Meta:
        verbose_name = u'Упоминание'
        verbose_name_plural = u'Упоминания'


class Tutorial(models.Model):
    title = models.CharField(u'Название обучающего материала', max_length=250)
    slug = models.SlugField(u'Слаг', default='')

    author = models.ForeignKey(Speaker, blank=True, null=True,
        verbose_name=u'Автор')

    description = models.TextField(u'Краткое описание')
    content = models.TextField(u'Содержание')

    def __str__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return 'tutorial', [self.slug]

    class Meta:
        verbose_name = u'Полезный материал'
        verbose_name_plural = u'Полезные материалы'


class Vote(TimeStampedModel):
    talk = models.ForeignKey(Talk, related_name='votes')
    event = models.ForeignKey(Event, related_name='votes')
    ua = models.TextField(u'User Agent')
    ip = models.TextField(u'IP')

    class Meta:
        verbose_name = u'Голос'
        verbose_name_plural = u'Голос'
