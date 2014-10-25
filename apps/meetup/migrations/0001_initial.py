# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import picklefield.fields
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('status', model_utils.fields.StatusField(no_check_for_status=True, verbose_name='status', default='planning', max_length=100, choices=[('planning', 'planning'), ('active', 'active'), ('archived', 'archived'), ('draft', 'draft')])),
                ('status_changed', model_utils.fields.MonitorField(verbose_name='status changed', monitor='status', default=django.utils.timezone.now)),
                ('name', models.CharField(verbose_name='Название', max_length=1024)),
                ('number', models.SmallIntegerField(null=True, blank=True, verbose_name='Номер')),
                ('description', models.TextField(verbose_name='Описание', blank=True)),
                ('image', models.ImageField(null=True, upload_to='events', blank=True, verbose_name='Изображение')),
                ('date', models.DateTimeField(null=True, blank=True, verbose_name='Начало')),
                ('timepad_id', models.IntegerField(verbose_name='ID события на Timepad', blank=True, default=0)),
                ('manual_on_air', models.NullBooleanField(verbose_name='Включить трансляцию', default=None, help_text='Включается автоматически за полчаса до начала и идёт 4 часа. Нужно, для тестирования в другое время.')),
                ('votable', models.BooleanField(verbose_name='Включить голосование', default=False)),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'Событие',
                'get_latest_by': 'number',
                'verbose_name_plural': 'События',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MediaCoverage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Название упоминания', max_length=250)),
                ('url', models.URLField(verbose_name='Адрес страницы с упоминанием')),
                ('ico', models.CharField(null=True, blank=True, max_length=250, verbose_name='Ссылка на .ico сайта')),
                ('event', models.ForeignKey(related_name='media_coverages', to='meetup.Event')),
            ],
            options={
                'verbose_name': 'Упоминание',
                'verbose_name_plural': 'Упоминания',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('url', models.URLField(verbose_name='Ссылка на внешнее фото', blank=True, help_text='Временное поле')),
                ('image', models.ImageField(verbose_name='Фотография', upload_to='photos', blank=True)),
                ('caption', models.TextField(verbose_name='Подпись', blank=True)),
                ('event', models.ForeignKey(null=True, related_name='photos', blank=True, to='meetup.Event')),
            ],
            options={
                'verbose_name': 'Фотография',
                'verbose_name_plural': 'Фотографии',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Имя', max_length=100)),
                ('slug', models.SlugField(verbose_name='Слаг', default='')),
                ('photo', models.ImageField(null=True, upload_to='speakers', blank=True, verbose_name='Фотография')),
                ('company_name', models.CharField(verbose_name='Название компании', blank=True, max_length=1024)),
                ('description', models.TextField(verbose_name='Описание', blank=True)),
            ],
            options={
                'verbose_name': 'Докладчик',
                'verbose_name_plural': 'Докладчики',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Название компании', max_length=250)),
                ('logo', models.ImageField(verbose_name='Логотип', upload_to='sponsors')),
                ('url', models.URLField(verbose_name='Адрес сайта', blank=True)),
                ('status', models.CharField(verbose_name='Тип', choices=[('organizer', 'organizer'), ('partner', 'partner')], max_length=10)),
            ],
            options={
                'verbose_name': 'Спонсор',
                'verbose_name_plural': 'Спонсоры',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('status', model_utils.fields.StatusField(no_check_for_status=True, verbose_name='status', default='active', max_length=100, choices=[('active', 'active'), ('draft', 'draft')])),
                ('status_changed', model_utils.fields.MonitorField(verbose_name='status changed', monitor='status', default=django.utils.timezone.now)),
                ('name', models.CharField(verbose_name='Название', max_length=1024)),
                ('slug', models.SlugField(verbose_name='Код')),
                ('description', models.TextField(verbose_name='Описание', blank=True)),
                ('presentation', models.URLField(verbose_name='Адрес презентации', blank=True)),
                ('presentation_data', picklefield.fields.PickledObjectField(verbose_name='Meta-данные презентации', blank=True, editable=False)),
                ('video', models.URLField(verbose_name='Адрес видео', blank=True)),
                ('video_data', picklefield.fields.PickledObjectField(verbose_name='Meta-данные видео', blank=True, editable=False)),
                ('position', models.SmallIntegerField(verbose_name='Порядок', default=0, help_text='Порядок выступления на событии')),
                ('event', models.ForeignKey(verbose_name='Событие', related_name='talks', to='meetup.Event')),
                ('speaker', models.ForeignKey(verbose_name='Докладчик', related_name='talks', to='meetup.Speaker')),
            ],
            options={
                'ordering': ('-event__number', 'position'),
                'verbose_name': 'Выступление',
                'verbose_name_plural': 'Выступления',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='Название обучающего материала', max_length=250)),
                ('slug', models.SlugField(verbose_name='Слаг', default='')),
                ('description', models.TextField(verbose_name='Краткое описание')),
                ('content', models.TextField(verbose_name='Содержание')),
                ('author', models.ForeignKey(null=True, verbose_name='Автор', blank=True, to='meetup.Speaker')),
            ],
            options={
                'verbose_name': 'Полезный материал',
                'verbose_name_plural': 'Полезные материалы',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Название места', max_length=100)),
                ('address', models.TextField(verbose_name='Адрес')),
                ('latitude', models.DecimalField(null=True, decimal_places=6, max_digits=9, blank=True, verbose_name='Широта')),
                ('longitude', models.DecimalField(null=True, decimal_places=6, max_digits=9, blank=True, verbose_name='Долгота')),
            ],
            options={
                'verbose_name': 'Место',
                'verbose_name_plural': 'Места',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('ua', models.TextField(verbose_name='User Agent')),
                ('ip', models.TextField(verbose_name='IP')),
                ('event', models.ForeignKey(related_name='votes', to='meetup.Event')),
                ('talk', models.ForeignKey(related_name='votes', to='meetup.Talk')),
            ],
            options={
                'verbose_name': 'Голос',
                'verbose_name_plural': 'Голос',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='sponsors',
            field=models.ManyToManyField(verbose_name='Спонсоры', blank=True, to='meetup.Sponsor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(null=True, blank=True, to='meetup.Venue'),
            preserve_default=True,
        ),
    ]
