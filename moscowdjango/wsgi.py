import os


def force_domain(fn):
    def wrapped(environ, start_response):
        domain = os.environ.get('DOMAIN')
        if domain and environ['HTTP_HOST'] != domain:
            path = environ.get('PATH_INFO', '')
            start_response('301 Redirect', [('Location', 'http://%s%s' % (domain, path)),])
            return []
        return fn(environ, start_response)
    return wrapped

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moscowdjango.settings")

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
application = force_domain(application)
