# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetup', '0002_event_registration_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='streaming_url',
            field=models.URLField(blank=True, verbose_name='Ссылка на трансляцию'),
            preserve_default=True,
        ),
    ]
