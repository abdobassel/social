import factory
from django.conf import settings

from social.posts.models import Post


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    password = "something-testing"
    email = "something@test.com"
    username = "test-some-username"
    is_staff = True
    is_superuser = True


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    user = factory.SubFactory(UserFactory)
    content = "some content"
    slug = "some-content"
    visibility = "EVERYONE"
