Deploy
------

1) Create a virtualenv

virtualenv ../moscowdjango.env

2) Install dependencies:

../moscowdjango.env/bin/pip install -r reqs.txt

3) Launch it

../moscowdjango.env/bin/python manage.py runserver


Useful dev commands
-------------------

python manage.py dumpdata meetup --format=json-pretty --indent=4 > meetup/fixtures/initial_data.json