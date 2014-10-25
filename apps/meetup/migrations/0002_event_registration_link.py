# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetup', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='registration_link',
            field=models.URLField(default='', verbose_name='Ссылка на событие', blank=True),
            preserve_default=False,
        ),
    ]
