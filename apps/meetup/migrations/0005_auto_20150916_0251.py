# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetup', '0004_auto_20150408_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='end_time',
            field=models.TimeField(null=True, blank=True, verbose_name='Время окончания'),
        ),
        migrations.AddField(
            model_name='talk',
            name='start_time',
            field=models.TimeField(null=True, blank=True, verbose_name='Время начала'),
        ),
    ]
