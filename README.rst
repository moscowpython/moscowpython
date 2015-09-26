Moscow Python Meetup site
=========================

Sources of https://moscowpython.ru (previously moscowdjango.ru)

.. image:: https://img.shields.io/travis/moscowpython/moscowpython/master.svg
    :target: https://travis-ci.org/moscowpython/moscowpython

.. image:: https://img.shields.io/coveralls/moscowpython/moscowpython/master.svg
    :target: https://coveralls.io/r/moscowpython/moscowpython/

.. image:: https://requires.io/github/moscowpython/moscowpython/requirements.svg?branch=master
     :target: https://requires.io/github/moscowpython/moscowpython/requirements/?branch=master

.. image:: https://img.shields.io/badge/python-3.4-blue.svg

.. image:: https://img.shields.io/badge/licence-BSD-blue.svg

Running locally
---------------

::

    git clone https://github.com/moscowpython/moscowpython/
    cd moscowpython
    pyenv env
    source env/bin/activate
    pip install -r requirements.txt
    npm install
    ./node_modules/.bin/gulp

    python manage.py syncdb
    python manage.py migrate
    python manage.py loaddata development.json  # convenient
    python manage.py runserver


Tests
-----
::

    tox
