# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetup', '0003_event_streaming_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='streaming_embed',
            field=models.TextField(blank=True, verbose_name='Embed трансляции', help_text='html с ютуба или другого источника'),
        ),
        migrations.AlterField(
            model_name='event',
            name='timepad_id',
            field=models.IntegerField(blank=True, verbose_name='ID события на Timepad', editable=False, default=0),
        ),
        migrations.AlterField(
            model_name='event',
            name='votable',
            field=models.BooleanField(verbose_name='Включить голосование', editable=False, default=False),
        ),
    ]
