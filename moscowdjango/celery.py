# coding: utf-8
import os

from celery import Celery

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moscowdjango.settings')

app = Celery('moscowdjango',
             backend=os.environ.get('CLOUDAMQP_URL', 'redis://localhost'),
             broker=os.environ.get('CLOUDAMQP_URL', 'redis://localhost'))

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
