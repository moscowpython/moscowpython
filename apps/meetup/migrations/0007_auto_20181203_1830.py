# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-12-03 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetup', '0006_auto_20160315_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='executive',
            name='company',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='executive',
            name='link',
            field=models.URLField(blank=True),
        ),
    ]
