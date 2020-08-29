# Django settings for moscowdjango project.
from .settings import *

DEBUG = False

EMBEDLY_KEY = os.environ.get('EMBEDLY_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

# Amazon credentials
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_QUERYSTRING_AUTH = False
AWS_CALLING_FORMAT = 2  # SUBDOMAIN
AWS_S3_SECURE_URLS = True

# Media & static
DEFAULT_FILE_STORAGE = 'moscowdjango.amazon.DefaultStorage'
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
DEFAULT_S3_PATH = "media"
MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
MEDIA_URL = 'https://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME

# Django compressor
COMPRESS_ENABLED = False
