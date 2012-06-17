import os
from barrel.basic import BasicAuth

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangodocs.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# http auth during private alpha
logins = [('django', 'uncha!ned')]
application = BasicAuth(application, users=logins)
