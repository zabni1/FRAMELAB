from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from main.views import ErrorView
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = ([
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  + debug_toolbar_urls())


handler404 = ErrorView