import pytest

from social.profiles.models import Profile
from social.users.models import User


@pytest.mark.django_db
def test_model_str_method():
    user = User.objects.create(username="johndoe")
    instance = Profile(user=user)
    expected_str = "johndoe"
    assert str(instance) == expected_str
