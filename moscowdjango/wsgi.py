import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moscowdjango.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

def force_domain(fn):
    def wrapped(environ, start_response):
        domain = os.environ.get('DOMAIN')
        if domain and environ['HTTP_HOST'] != domain:
            path = environ.get('PATH_INFO', '')
            start_response('301 Redirect', [('Location', 'http://%s%s' % (domain, path)),])
            return []
        return fn(environ, start_response)
    return wrapped

application = force_domain(application)
