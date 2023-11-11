from django.urls import path

from .follows import FollowersAPIView, FollowingAPIView, UnfollowAPIView, FollowAPIView
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
    # Following
    path("me/followers/", FollowersAPIView.as_view(), name="followers"),
    path("<int:pk>/follow/", FollowingAPIView.as_view(), name="follow"),
    path("<int:pk>/unfollow/", UnfollowAPIView.as_view(), name="unfollow"),
    path("<int:pk>/-F-follow/", FollowAPIView.as_view(), name="follow-f"),

]
