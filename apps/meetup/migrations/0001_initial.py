# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import picklefield.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('status', model_utils.fields.StatusField(max_length=100, no_check_for_status=True, choices=[('planning', 'planning'), ('active', 'active'), ('archived', 'archived'), ('draft', 'draft')], verbose_name='status', default='planning')),
                ('status_changed', model_utils.fields.MonitorField(monitor='status', verbose_name='status changed', default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=1024, verbose_name='Название')),
                ('number', models.SmallIntegerField(verbose_name='Номер', blank=True, null=True)),
                ('description', models.TextField(verbose_name='Описание', blank=True)),
                ('image', models.ImageField(verbose_name='Изображение', upload_to='events', blank=True, null=True)),
                ('date', models.DateTimeField(verbose_name='Начало', blank=True, null=True)),
                ('timepad_id', models.IntegerField(verbose_name='ID события на Timepad', blank=True, default=0)),
                ('manual_on_air', models.NullBooleanField(help_text='Включается автоматически за полчаса до начала и идёт 4 часа. Нужно, для тестирования в другое время.', verbose_name='Включить трансляцию', default=None)),
                ('votable', models.BooleanField(verbose_name='Включить голосование', default=False)),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name_plural': 'События',
                'verbose_name': 'Событие',
                'get_latest_by': 'number',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MediaCoverage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=250, verbose_name='Название упоминания')),
                ('url', models.URLField(verbose_name='Адрес страницы с упоминанием')),
                ('ico', models.CharField(max_length=250, verbose_name='Ссылка на .ico сайта', blank=True, null=True)),
                ('event', models.ForeignKey(to='meetup.Event')),
            ],
            options={
                'verbose_name_plural': 'Упоминания',
                'verbose_name': 'Упоминание',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('url', models.URLField(help_text='Временное поле', verbose_name='Ссылка на внешнее фото', blank=True)),
                ('image', models.ImageField(verbose_name='Фотография', upload_to='photos', blank=True)),
                ('caption', models.TextField(verbose_name='Подпись', blank=True)),
                ('event', models.ForeignKey(to='meetup.Event', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Фотографии',
                'verbose_name': 'Фотография',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('slug', models.SlugField(verbose_name='Слаг', default='')),
                ('photo', models.ImageField(verbose_name='Фотография', upload_to='speakers', blank=True, null=True)),
                ('company_name', models.CharField(max_length=1024, verbose_name='Название компании', blank=True)),
                ('description', models.TextField(verbose_name='Описание', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Докладчики',
                'verbose_name': 'Докладчик',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=250, verbose_name='Название компании')),
                ('logo', models.ImageField(verbose_name='Логотип', upload_to='sponsors')),
                ('url', models.URLField(verbose_name='Адрес сайта', blank=True)),
                ('status', models.CharField(max_length=10, choices=[('organizer', 'organizer'), ('partner', 'partner')], verbose_name='Тип')),
            ],
            options={
                'verbose_name_plural': 'Спонсоры',
                'verbose_name': 'Спонсор',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='sponsors',
            field=models.ManyToManyField(to='meetup.Sponsor', verbose_name='Спонсоры', blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('status', model_utils.fields.StatusField(max_length=100, no_check_for_status=True, choices=[('active', 'active'), ('draft', 'draft')], verbose_name='status', default='active')),
                ('status_changed', model_utils.fields.MonitorField(monitor='status', verbose_name='status changed', default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=1024, verbose_name='Название')),
                ('slug', models.SlugField(verbose_name='Код')),
                ('description', models.TextField(verbose_name='Описание', blank=True)),
                ('presentation', models.URLField(verbose_name='Адрес презентации', blank=True)),
                ('presentation_data', picklefield.fields.PickledObjectField(editable=False, verbose_name='Meta-данные презентации', blank=True)),
                ('video', models.URLField(verbose_name='Адрес видео', blank=True)),
                ('video_data', picklefield.fields.PickledObjectField(editable=False, verbose_name='Meta-данные видео', blank=True)),
                ('position', models.SmallIntegerField(help_text='Порядок выступления на событии', verbose_name='Порядок', default=0)),
                ('event', models.ForeignKey(to='meetup.Event', verbose_name='Событие')),
                ('speaker', models.ForeignKey(to='meetup.Speaker', verbose_name='Докладчик')),
            ],
            options={
                'ordering': ('-event__number', 'position'),
                'verbose_name_plural': 'Выступления',
                'verbose_name': 'Выступление',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=250, verbose_name='Название обучающего материала')),
                ('slug', models.SlugField(verbose_name='Слаг', default='')),
                ('description', models.TextField(verbose_name='Краткое описание')),
                ('content', models.TextField(verbose_name='Содержание')),
                ('author', models.ForeignKey(to='meetup.Speaker', verbose_name='Автор', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Полезные материалы',
                'verbose_name': 'Полезный материал',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Название места')),
                ('address', models.TextField(verbose_name='Адрес')),
                ('latitude', models.DecimalField(max_digits=9, verbose_name='Широта', decimal_places=6, blank=True, null=True)),
                ('longitude', models.DecimalField(max_digits=9, verbose_name='Долгота', decimal_places=6, blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Места',
                'verbose_name': 'Место',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(to='meetup.Venue', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('ua', models.TextField(verbose_name='User Agent')),
                ('ip', models.TextField(verbose_name='IP')),
                ('event', models.ForeignKey(to='meetup.Event')),
                ('talk', models.ForeignKey(to='meetup.Talk')),
            ],
            options={
                'verbose_name_plural': 'Голос',
                'verbose_name': 'Голос',
            },
            bases=(models.Model,),
        ),
    ]
