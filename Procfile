web: python manage.py runserver --settings=moscowdjango.settings_production "0.0.0.0:$PORT"
worker: celery worker --app=moscowdjango --loglevel=info -B
