from django.conf import settings
from storages.backends.s3 import S3Storage


class StaticStorage(S3Storage):
    """
    Storage for static files.
    The folder is defined in settings.STATIC_S3_PATH
    """

    def __init__(self, *args, **kwargs):
        kwargs['location'] = settings.STATIC_S3_PATH
        super(StaticStorage, self).__init__(*args, **kwargs)


class DefaultStorage(S3Storage):
    """
    Storage for uploaded media files.
    The folder is defined in settings.DEFAULT_S3_PATH
    """

    def __init__(self, *args, **kwargs):
        kwargs['location'] = settings.DEFAULT_S3_PATH
        super(DefaultStorage, self).__init__(*args, **kwargs)