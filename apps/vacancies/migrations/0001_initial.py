# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('status', model_utils.fields.StatusField(max_length=100, no_check_for_status=True, choices=[('active', 'active'), ('draft', 'draft')], verbose_name='status', default='active')),
                ('status_changed', model_utils.fields.MonitorField(monitor='status', verbose_name='status changed', default=django.utils.timezone.now)),
                ('company', models.CharField(max_length=100, verbose_name='Компания')),
                ('name', models.CharField(max_length=100, verbose_name='Должность')),
                ('salary', models.CharField(max_length=100, verbose_name='З/П', blank=True)),
                ('url', models.URLField(unique=True, verbose_name='Внешняя ссылка')),
                ('published_at', models.DateTimeField(verbose_name='Дата публикации', null=True)),
                ('description', models.TextField(help_text='Markdown', verbose_name='Текст', blank=True)),
                ('contacts', models.TextField(help_text='Markdown', verbose_name='Контакты', blank=True)),
                ('type', models.CharField(max_length=50, choices=[('fulltime', 'Фултайм'), ('contract', 'Контракт')], verbose_name='Занятость', default='fulltime')),
                ('is_participant', models.BooleanField(verbose_name='На митапе', default=False)),
                ('is_priority', models.BooleanField(verbose_name='Приоритетная вакансия', default=False)),
            ],
            options={
                'ordering': ['-is_priority', '-published_at'],
                'verbose_name_plural': 'Вакансии',
                'verbose_name': 'Вакансия',
            },
            bases=(models.Model,),
        ),
    ]
