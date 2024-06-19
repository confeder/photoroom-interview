import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def _auto_use_db(db):
    pass


@pytest.fixture
def user_a() -> User:
    return User.objects.create(
        username="demo@demo.com", email="demo@demo.com", is_superuser=True
    )


@pytest.fixture
def user_a_client(user_a):
    client = APIClient()
    client.force_authenticate(user_a)
    return client
