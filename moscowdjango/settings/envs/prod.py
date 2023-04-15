from __future__ import annotations

from configurations import values

from moscowdjango.settings.envs.staging import Staging


class Prod(Staging):
    DEBUG = False  # noqa: allowed straight assignment

    SECRET_KEY = values.SecretValue()

    CSRF_TRUSTED_ORIGINS = values.ListValue(['https://moscowpython.ru', 'https://www.moscowpython.ru'])

    ALLOWED_HOSTS = values.ListValue(['moscowpython.ru', 'www.moscowpython.ru', 'msk.python.ru'])
