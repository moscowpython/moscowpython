from __future__ import annotations

from invoke import task


@task
def update_requirements(cmd):
    cmd.run('python -m pip install --upgrade pip-tools')
    cmd.run('pip-compile --generate-hashes --no-emit-index-url --allow-unsafe requirements/base.in')
    cmd.run('pip-compile --generate-hashes --no-emit-index-url --allow-unsafe requirements/dev.in')


@task
def install_requirements(cmd):
    cmd.run('python -m pip install --upgrade pip-tools')
    cmd.run('pip-sync requirements/base.txt requirements/dev.txt')


@task
def precommit(cmd):
    cmd.run('pre-commit install -t pre-commit -t commit-msg')


@task
def makemigrations(cmd):
    cmd.run('python3 manage.py makemigrations')


@task
def migrate(cmd):
    cmd.run('python3 manage.py migrate')


@task
def frontend(cmd):
    cmd.run('npm install')
    cmd.run('npx gulp compile')
    cmd.run('mkdir -p moscowdjango/static')
    cmd.run('cp -R build/* moscowdjango/static/')


@task
def run(cmd):
    cmd.run('python3 manage.py runserver')


@task
def check(cmd):
    cmd.run('python ./manage.py makemigrations --dry-run --check')
    cmd.run('flake8 .')


@task
def test(cmd):
    cmd.run('DJANGO_CONFIGURATION=Test python -m pytest')


@task
def shell(cmd):
    cmd.run('python manage.py shell_plus', pty=True)
