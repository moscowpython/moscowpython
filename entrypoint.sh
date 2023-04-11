#!/bin/bash

if [ -z "$1" ]
  then
    echo "No argument supplied"
    exit 1
elif [ $1 = "pre-run" ]
  then
    python manage.py collectstatic --noinput
    python manage.py migrate
elif [ $1 = "runserver" ]
  then
    exec gunicorn --bind 0.0.0.0:8000 \
                  --worker-tmp-dir /dev/shm \
                  --access-logfile - \
                  --error-logfile - \
                  --log-level info \
                  --workers 5 \
                  moscowdjango.wsgi:application
    exit $?
else
  echo "Invalid argument $1"
  exit 1
fi
