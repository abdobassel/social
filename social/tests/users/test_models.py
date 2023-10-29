import pytest

from social.users.models import User


@pytest.mark.django_db
def test_model_str_method():
    instance = User(first_name="John", last_name="Doe")
    expected_str = "John Doe"
    assert str(instance) == expected_str
