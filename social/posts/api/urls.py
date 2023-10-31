from django.urls import path

from .views import PostCreateAPIView, PostHashtagListAPIView, PostListAPIView, PostUpdateAPIView, PostDeleteAPIView

urlpatterns = [
    path("post/", PostListAPIView.as_view(), name="post-list"),
    path("C-/post/", PostCreateAPIView.as_view(), name="c-post-list"),
    path("U-/post/<int:post_id>/", PostUpdateAPIView.as_view(), name="post-update"),
    path("D-/post/<int:post_id>/", PostDeleteAPIView.as_view(), name="post-delete"),
    path("hashtags/", PostHashtagListAPIView.as_view(), name="post-hashtag-list"),
]
