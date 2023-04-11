from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views.generic.base import TemplateView

handler500 = TemplateView.as_view(template_name="500.html")

urlpatterns = [path('', include('apps.meetup.urls')), re_path(r'^admin/', admin.site.urls)]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
