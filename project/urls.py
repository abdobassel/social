from denied.decorators import allow
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/v1/rest/", include("rest_framework.urls")),
    path("auth/", include("djoser.urls")),
    path("api-auth/", include("social.users.urls")),
]

# Enable the debug toolbar only in DEBUG mode.
if settings.DEBUG and settings.DEBUG_TOOLBAR:
    urlpatterns = [
                      path("__debug__/", allow(include("debug_toolbar.urls"))),
                  ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
