Moscow Django Meetup site
=========================

Sources of http://moscowdjango.ru

.. image:: https://secure.travis-ci.org/futurecolors/moscowdjango.png?branch=master
    :target: https://travis-ci.org/futurecolors/moscowdjango

.. image:: https://coveralls.io/repos/futurecolors/moscowdjango/badge.png?branch=master
    :target: https://coveralls.io/r/futurecolors/moscowdjango/

.. image:: https://requires.io/github/futurecolors/moscowdjango/requirements.png?branch=master
    :target: https://requires.io/github/futurecolors/moscowdjango/requirements/?branch=master
    :alt: Requirements Status


Running locally
---------------

Python 3.4+ required

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

    python manage.py test
