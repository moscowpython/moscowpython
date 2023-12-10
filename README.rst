Moscow Python Meetup site
=========================

Sources of https://moscowpython.ru (previously moscowdjango.ru)


Running locally
---------------

::

    git clone git@github.com:moscowpython/moscowpython.git
    cd moscowpython
    python -m venv env
    source env/bin/activate
    pip install pip-tools invoke
    invoke install-requirements

    inv migrate
    python manage.py loaddata development.json
    inv run


Tests
-----
::

    inv check
    inv test

Pre-commit
----------

To install pre-commit hooks, run::

    inv precommit
