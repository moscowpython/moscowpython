from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView
from settings import STATIC_ROOT

admin.autodiscover()

handler500 = TemplateView.as_view(template_name="500.html")

urlpatterns = patterns('',
    url(r'^(favicon.ico)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'', include('meetup.urls')),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)