from django.urls import path

from .views import (
    ProfileListAPIView,
    ProfileRetrieveAPIView,
    ProfileUpdateAPIView,
    ProfilePhotoAPIView,
)

app_name = "profiles"
urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), name="all-profiles"),
    path("me/", ProfileRetrieveAPIView.as_view(), name="my-profile"),
    path("update/", ProfileUpdateAPIView.as_view(), name="update-profile"),
    path("photo/<int:pk>/", ProfilePhotoAPIView.as_view(), name="photo-profile-api"),
]
