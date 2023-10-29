from django.urls import path

from .views import PostHashtagListAPIView, PostListAPIView

urlpatterns = [
    path("post/", PostListAPIView.as_view(), name="post-list"),
    path("hashtags/", PostHashtagListAPIView.as_view(), name="post-hashtag-list"),
]
