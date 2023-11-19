# from django.contrib.auth import get_user_model
# from django.test import TestCase
#
# from social.posts.models import Post, Like, PostHashtag
#
#
# class PostModelTest(TestCase):
#     def setUp(self):
#         # Create a test user
#         self.user = get_user_model().objects.create_user(
#             email="testemail@example.com", username="testuser", password="test-password"
#         )
#
#         # Create a test hashtag
#         self.hashtag = PostHashtag.objects.create(name="test-hashtag", slug="test-hashtag")
#
#         # Create a test post
#         self.post = Post.objects.create(
#             user=self.user,
#             content="Test content",
#             slug="test-slug",
#             location="Test location",
#             visibility=Post.Visibility.EVERYONE,
#         )
#
#     def test_post_creation(self):
#         """Test that a post is created correctly."""
#         self.assertEqual(str(self.post), "Test ")  # Check the __str__ method
#
#     def test_like_creation(self):
#         """Test that a like is created correctly."""
#         like = Like.objects.create(user=self.user, post=self.post)
#         self.assertEqual(like.user, self.user)
#         self.assertEqual(like.post, self.post)
#
#     def test_post_hashtag_creation(self):
#         """Test that a post hashtag is created correctly."""
#         self.assertEqual(str(self.hashtag), "test-hashtag")
#
#     # Add more tests as needed for your specific requirements
import pytest
from django.contrib.auth import get_user_model

from social.posts.models import Post, Like, PostHashtag


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(
        email="testemail@example.com",
        username="testuser",
        password="test-password",
    )


@pytest.fixture
def hashtag(db):
    return PostHashtag.objects.create(name="test-hashtag", slug="test-hashtag")


@pytest.fixture
def post(user, hashtag):
    return Post.objects.create(
        user=user,
        content="Test that a post is created correctly.",
        slug="test-slug",
        location="Test location",
        visibility=Post.Visibility.EVERYONE,
    )


@pytest.mark.django_db
def test_post_creation(post):
    """Test that a post is created correctly."""
    assert str(post) == "Test "


@pytest.mark.django_db
def test_like_creation(user, post):
    """Test that a like is created correctly."""
    like = Like.objects.create(user=user, post=post)
    assert like.user == user
    assert like.post == post


@pytest.mark.django_db
def test_post_hashtag_creation(hashtag):
    """Test that a post-hashtag is created correctly."""
    assert str(hashtag) == "test-hashtag"

# Add more tests as needed for your specific requirements
