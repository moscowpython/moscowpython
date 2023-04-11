from __future__ import annotations

from moscowdjango.settings.envs.dev import Dev


class Test(Dev):
    DEBUG = True  # noqa: allowed straight assignment

    STORAGES = {
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'django.core.files.storage.StaticFilesStorage'},
    }
