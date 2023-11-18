from denied.decorators import allow
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls")),
    # LOCAL APPS
    path("auth/", include("social.users.urls")),
    path("posts/", include("social.posts.api.urls")),
    path("profiles/", include("social.profiles.api.urls")),
    path("messages/", include("social.private_message.api.urls")),
]

# Enable the debug toolbar only in DEBUG mode.
if settings.DEBUG and settings.DEBUG_TOOLBAR:
    urlpatterns = [
                      path("__debug__/", allow(include("debug_toolbar.urls"))),
                  ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
