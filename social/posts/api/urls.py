from django.urls import path

from .views import (
    PostCreateAPIView,
    PostHashtagListCreateAPIView,
    UserListByHashtagAPIView,
    PostListAPIView,
    PostUpdateAPIView,
    PostDeleteAPIView,
    PostPhotoRetrieveUpdateDestroyAPIView,
    PostPhotoCreateAPIView,
    LikePostAPIView,
)

urlpatterns = [
    path("post/", PostListAPIView.as_view(), name="post-list"),
    path("C-/post/", PostCreateAPIView.as_view(), name="create-post-list"),
    path("C-/post/<int:pk>/", PostPhotoRetrieveUpdateDestroyAPIView.as_view(), name="post-photo-update-delete"),
    path("photo/create/", PostPhotoCreateAPIView.as_view(), name="create-post-with-photo"),
    path("U-/post/<int:post_id>/", PostUpdateAPIView.as_view(), name="post-update"),
    path("D-/post/<int:post_id>/", PostDeleteAPIView.as_view(), name="post-delete"),
    path("hashtags/", PostHashtagListCreateAPIView.as_view(), name="hashtag-list-retrieve"),
    path("hashtags/<str:hashtag_name>/users/", UserListByHashtagAPIView.as_view(), name="user-list-by-hashtag"),
    path("like/<int:post_id>/", LikePostAPIView.as_view(), name="like-post"),
]
