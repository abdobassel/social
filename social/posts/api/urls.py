from django.urls import path

from .views import PostHashtagListAPIView, PostListAPIView, PostListCreateView

urlpatterns = [
    path("post/", PostListAPIView.as_view(), name="post-list"),
    path("C-/post/", PostListCreateView.as_view(), name="c-post-list"),
    path("hashtags/", PostHashtagListAPIView.as_view(), name="post-hashtag-list"),
]
