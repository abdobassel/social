import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework.request import Request

from social.posts.api.serializers import UserSerializer, PostHashtagSerializer, PostFileMediaSerializer
from social.posts.models import Post, PostHashtag


# from social.posts.serializers import PostSerializer, PostHashtagSerializer, UserSerializer, PostFileMediaSerializer


@pytest.fixture
def user():
    return baker.make(get_user_model(), username="testuser")


@pytest.fixture
def post(user):
    return baker.make(Post, user=user, content="Test content")


@pytest.fixture
def hashtag():
    return baker.make(PostHashtag, name="test-hashtag", slug="test-hashtag", is_active=True)


def test_user_serializer():
    user = baker.make(get_user_model())
    serializer = UserSerializer(user)
    assert "id" in serializer.data
    assert "username" in serializer.data


def test_post_hashtag_serializer():
    hashtag = baker.make(PostHashtag, name="test-hashtag", slug="test-hashtag", is_active=True)
    serializer = PostHashtagSerializer(hashtag)
    assert "id" in serializer.data
    assert "name" in serializer.data
    assert "slug" in serializer.data
    assert "is_active" in serializer.data


def test_post_file_media_serializer(post):
    serializer = PostFileMediaSerializer(post)
    assert "id" in serializer.data
    assert "post_photo" in serializer.data
    assert "user" in serializer.data
    assert "likes" in serializer.data
    assert "hashtags" in serializer.data
    assert "views" in serializer.data


def test_post_serializer(user, hashtag):
    request = Request()
    data = {
        "user": user.id,
        "content": "Test content",
        "hashtags": [{"name": hashtag.name, "slug": hashtag.slug, "is_active": hashtag.is_active}],
    }
    serializer = PostSerializer(data=data, context={"request": request})
    assert serializer.is_valid()
    post = serializer.save()

    assert post.user == user
    assert post.content == "Test content"
    assert post.hashtags.count() == 1
    assert post.hashtags.first() == hashtag
    assert post.likes_count == 0
