from __future__ import annotations

import datetime
from urllib.parse import urljoin

from django.conf import settings
from django.db import models
from django.db.models.manager import Manager
from django.urls import reverse
from model_utils import Choices
from model_utils.managers import QueryManager
from model_utils.models import StatusModel, TimeStampedModel
from picklefield.fields import PickledObjectField
from apps.meetup.embed import get_embed_data


class TalkManager(Manager):
    def active(self):
        qs = self.get_queryset()
        return qs.filter(status='active').exclude(event__status="draft")


class SponsorManager(Manager):
    def partners(self):
        qs = self.get_queryset()
        return qs.filter(status="partner")

    def organizers(self):
        qs = self.get_queryset()
        return qs.filter(status="organizer")


class Talk(StatusModel):
    STATUS = Choices('active', 'draft')

    name = models.CharField('Название', max_length=1024)
    speaker = models.ForeignKey('Speaker', on_delete=models.CASCADE, verbose_name='Докладчик', related_name='talks')
    event = models.ForeignKey('Event', on_delete=models.CASCADE, verbose_name='Событие', related_name='talks')
    slug = models.SlugField('Код')
    description = models.TextField('Описание', null=True, blank=True)
    presentation = models.URLField('Адрес презентации', null=True, blank=True)
    presentation_data = PickledObjectField('Meta-данные презентации', editable=True, blank=True, null=True)
    video = models.URLField('Адрес видео', null=True, blank=True)
    video_data = PickledObjectField('Meta-данные видео', null=True, blank=True)
    position = models.SmallIntegerField('Порядок', help_text='Порядок выступления на событии', default=0)

    start_time = models.TimeField('Время начала', blank=True, null=True)
    end_time = models.TimeField('Время окончания', blank=True, null=True)

    objects = TalkManager()

    original_presentation = None
    original_video = None

    def __init__(self, *args, **kwargs):
        super(Talk, self).__init__(*args, **kwargs)
        self.original_presentation = self.presentation
        self.original_video = self.video

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('talk', kwargs={'event_number': self.event.number, 'talk_slug': self.slug})

    def set_embedly_data(self, field_name, force=False):
        original_field_value = getattr(self, 'original_{0}'.format(field_name))
        new_field_value = getattr(self, field_name)
        if new_field_value != original_field_value or force:
            data_field_name = '{0}_data'.format(field_name)
            if new_field_value:
                data = get_embed_data(new_field_value)
                if data is not None:
                    setattr(self, data_field_name, data)
                return data
            else:
                setattr(self, data_field_name, "")
        setattr(self, 'original_{0}'.format(field_name), new_field_value)

    def save(self, *args, **kwargs):
        self.set_embedly_data('presentation')
        self.set_embedly_data('video')
        super(Talk, self).save(*args, **kwargs)

    # TODO: Add to talks normal timing
    def get_time_start(self):
        if self.start_time:
            return self.start_time
        return self.event.date + datetime.timedelta(minutes=40 * self.position)

    def get_time_end(self):
        if self.end_time:
            return self.end_time
        return self.event.date + datetime.timedelta(minutes=(40 * (self.position + 1)))

    class Meta:
        verbose_name = 'Выступление'
        verbose_name_plural = 'Выступления'
        ordering = ('-event__number', 'position')


class Event(StatusModel):
    """Events
    * draft - totally invisible
    * planning - only event description is shown
    * active - event is scheduled, speakers also visible
    * archived - event passed, registration is disabled
    """

    STATUS = Choices('planning', 'active', 'archived', 'draft')

    name = models.CharField('Название', max_length=1024)
    number = models.SmallIntegerField('Номер', blank=True, null=True)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение', upload_to='events', null=True, blank=True)
    date = models.DateTimeField('Начало', blank=True, null=True)
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE, blank=True, null=True)
    sponsors = models.ManyToManyField('Sponsor', verbose_name='Спонсоры', blank=True)
    registration_link = models.URLField('Ссылка на событие', blank=True)
    streaming_url = models.URLField('Ссылка на трансляцию', blank=True)
    streaming_embed = models.TextField('Embed трансляции', blank=True, help_text='html с ютуба или другого источника')
    manual_on_air = models.BooleanField(
        'Включить трансляцию',
        default=None,
        null=True,
        help_text='Включается автоматически за полчаса до начала и идёт 4 часа.',
    )

    # Deprecated:
    timepad_id = models.IntegerField('ID события на Timepad', blank=True, default=0, editable=False)
    votable = models.BooleanField('Включить голосование', default=False, editable=False)

    objects = Manager()
    visible = QueryManager(status__in=[STATUS.planning, STATUS.active, STATUS.archived])
    future = QueryManager(status__in=[STATUS.planning, STATUS.active])

    def __str__(self):
        if self.number:
            return f'{self.name} №{self.number}'
        else:
            return self.name

    def __repr__(self):
        return f'<Event №{self.number}>'

    def get_absolute_url(self):
        return reverse('event', kwargs={'number': self.number})

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
            return f'https://moscowdjango.timepad.ru/event/{self.timepad_id}/'
        if self.registration_link:
            return self.registration_link

    @classmethod
    def spotlight(cls, with_drafts=False):
        """Last active or last planned or last archived"""
        try:
            if with_drafts:
                return Event.objects.latest()
            return Event.future.latest()
        except Event.DoesNotExist:
            return None

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        get_latest_by = 'number'
        ordering = ['-date']


class Venue(models.Model):
    name = models.CharField('Название места', max_length=100)
    address = models.TextField('Адрес')
    latitude = models.DecimalField('Широта', decimal_places=6, max_digits=9, blank=True, null=True)
    longitude = models.DecimalField('Долгота', decimal_places=6, max_digits=9, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'


class Speaker(models.Model):
    name = models.CharField('Имя', max_length=100)
    slug = models.SlugField('Слаг', default='')
    photo = models.ImageField('Фотография', upload_to='speakers', null=True, blank=True)
    company_name = models.CharField('Название компании', max_length=1024, blank=True)
    description = models.TextField('Описание', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('speaker', kwargs={'slug': self.slug})

    @property
    def avatar_url(self):
        if settings.DEBUG:
            return urljoin(settings.STATIC_URL, 'images/avatars/reinhardt.png')
        if self.photo:
            return self.photo.url
        else:
            return urljoin(settings.STATIC_URL, 'images/avatars/reinhardt.png')

    class Meta:
        verbose_name = 'Докладчик'
        verbose_name_plural = 'Докладчики'
        ordering = ['name', '-pk']


class Photo(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='photos', blank=True, null=True)
    url = models.URLField('Ссылка на внешнее фото', help_text=u'Временное поле', blank=True)
    image = models.ImageField('Фотография', upload_to='photos', blank=True)
    caption = models.TextField('Подпись', blank=True)

    def __str__(self):
        return self.caption or f'Фото №{self.id}'

    def get_absolute_url(self):
        if self.url:
            return self.url
        else:
            return self.image.url

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'


class Sponsor(models.Model):
    STATUSES = Choices('organizer', 'partner')

    name = models.CharField('Название компании', max_length=250)
    logo = models.ImageField('Логотип', upload_to='sponsors')
    url = models.URLField('Адрес сайта', blank=True)
    status = models.CharField('Тип', choices=STATUSES, max_length=10)

    objects = SponsorManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.url

    class Meta:
        verbose_name = 'Спонсор'
        verbose_name_plural = 'Спонсоры'


class MediaCoverage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='media_coverages')
    name = models.CharField('Название упоминания', max_length=250)
    url = models.URLField('Адрес страницы с упоминанием')
    ico = models.CharField('Ссылка на .ico сайта', max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.url

    class Meta:
        verbose_name = 'Упоминание'
        verbose_name_plural = 'Упоминания'


class Tutorial(models.Model):
    title = models.CharField('Название обучающего материала', max_length=250)
    slug = models.SlugField('Слаг', default='')

    author = models.ForeignKey(Speaker, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Автор')

    description = models.TextField('Краткое описание')
    content = models.TextField('Содержание')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tutorial', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Полезный материал'
        verbose_name_plural = 'Полезные материалы'


class Vote(TimeStampedModel):
    talk = models.ForeignKey(Talk, on_delete=models.CASCADE, related_name='votes')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='votes')
    ua = models.TextField('User Agent')
    ip = models.TextField('IP')

    class Meta:
        verbose_name = 'Голос'
        verbose_name_plural = 'Голос'


class Executive(models.Model):
    name = models.CharField(max_length=64)
    company = models.CharField(max_length=64, blank=True)
    link = models.URLField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'
        ordering = ['order']

    def __str__(self):
        return self.name
