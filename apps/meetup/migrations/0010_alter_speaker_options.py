# Generated by Django 4.2.7 on 2024-01-13 14:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [('meetup', '0009_alter_talk_description_alter_talk_presentation_and_more')]

    operations = [
        migrations.AlterModelOptions(
            name='speaker',
            options={'ordering': ['name', '-pk'], 'verbose_name': 'Докладчик', 'verbose_name_plural': 'Докладчики'},
        )
    ]
