from __future__ import annotations

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moscowdjango.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

from configurations.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
