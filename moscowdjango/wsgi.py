import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moscowdjango.settings")

from django.core.wsgi import get_wsgi_application
_application = get_wsgi_application()


def application(environ, start_response):
    """ Redirecting all requests to canonical domain for additional ones"""
    domain = os.environ.get('DOMAIN')
    if domain and environ['HTTP_HOST'] != domain:
        path = environ.get('PATH_INFO')
        start_response('301 Redirect', [('Location', 'http://%s%s' % (domain, path)),])
        return []
    return _application(environ, start_response)
