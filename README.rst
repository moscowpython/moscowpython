Moscow Django Meetup site
=========================

Sources of https://moscowdjango.ru

.. image:: https://img.shields.io/travis/moscowdjango/moscowdjango/master.svg
    :target: https://travis-ci.org/moscowdjango/moscowdjango

.. image:: https://img.shields.io/coveralls/moscowdjango/moscowdjango/master.svg
    :target: https://coveralls.io/r/moscowdjango/moscowdjango/

.. image:: https://requires.io/github/moscowdjango/moscowdjango/requirements.svg?branch=master
     :target: https://requires.io/github/moscowdjango/moscowdjango/requirements/?branch=master

.. image:: https://img.shields.io/badge/python-3.4-blue.svg

.. image:: https://img.shields.io/badge/licence-BSD-blue.svg

Running locally
---------------

::

    git clone https://github.com/moscowdjango/moscowdjango/
    cd moscowdjango
    pyenv env
    source env/bin/activate
    pip install -r requirements.txt
    npm install
    ./node_modules/.bin/gulp

    python manage.py syncdb
    python manage.py migrate
    python manage.py loaddata development.json  # convenient
    python manage.py runsslserver


Tests
-----
::

    tox
