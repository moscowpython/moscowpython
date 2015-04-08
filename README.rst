Moscow Django Meetup site
=========================

Sources of https://moscowdjango.ru

.. image:: https://img.shields.io/travis/futurecolors/moscowdjango/master.svg
    :target: https://travis-ci.org/futurecolors/moscowdjango

.. image:: https://img.shields.io/coveralls/futurecolors/moscowdjango/master.svg
    :target: https://coveralls.io/r/futurecolors/moscowdjango/

.. image:: https://requires.io/github/futurecolors/moscowdjango/requirements.svg?branch=master
     :target: https://requires.io/github/futurecolors/moscowdjango/requirements/?branch=master

.. image:: https://img.shields.io/badge/python-3.4-blue.svg

.. image:: https://img.shields.io/badge/licence-BSD-blue.svg

Running locally
---------------

::

    git clone https://github.com/futurecolors/moscowdjango/
    cd moscowdjango
    pyenv env
    source env/bin/activate
    pip install -r requiremets.txt
    python manage.py syncdb
    python manage.py migrate
    python manage.py loaddata development.json  # convenient
    python manage.py runserver


Tests
-----
::

    tox
