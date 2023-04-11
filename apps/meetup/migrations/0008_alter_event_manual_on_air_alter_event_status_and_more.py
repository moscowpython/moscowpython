# Generated by Django 4.2 on 2023-04-11 09:43

from django.db import migrations, models
import model_utils.fields


class Migration(migrations.Migration):
    dependencies = [('meetup', '0007_auto_20181203_1830')]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='manual_on_air',
            field=models.BooleanField(
                default=None,
                help_text='Включается автоматически за полчаса до начала и идёт 4 часа.',
                null=True,
                verbose_name='Включить трансляцию',
            ),
        ),
        migrations.AlterField(
            model_name='event',
            name='status',
            field=model_utils.fields.StatusField(
                choices=[('planning', 'planning'), ('active', 'active'), ('archived', 'archived'), ('draft', 'draft')],
                default='planning',
                max_length=100,
                no_check_for_status=True,
                verbose_name='status',
            ),
        ),
        migrations.AlterField(
            model_name='talk',
            name='status',
            field=model_utils.fields.StatusField(
                choices=[('active', 'active'), ('draft', 'draft')],
                default='active',
                max_length=100,
                no_check_for_status=True,
                verbose_name='status',
            ),
        ),
    ]