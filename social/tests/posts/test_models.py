import pytest

from social.posts.models import Post
from social.tests.users.factories import PostFactory


@pytest.mark.django_db
class TestPostModel:
    def test_generate_slug_signal(self):
        # Create an instance of YourModel with a content value
        instance = PostFactory(content="some content")

        # Save the instance
        instance.save()
        instance = Post.objects.get(id=instance.id)
        # Check that the slug was generated correctly
        expected_slug = "some-content"
        assert instance.slug == expected_slug

    def test_str_return(self, post_factory):
        post = post_factory(content="some content")
        assert post.__str__() == "some "
