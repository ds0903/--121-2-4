import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from university_schedule.core.models import Group

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    def make_user(username, role):
        return User.objects.create_user(
            username=username,
            password="pass1234",
            email=f"{username}@example.com",
            role=role
        )
    return make_user

@pytest.fixture
def auth_client(api_client, create_user):
    def make_auth(username, role):
        user = create_user(username, role)
        # логін через DRF TokenAuth
        response = api_client.post("/api/users/login/", {
            "username": username, "password": "pass1234"
        })
        token = response.data["token"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        return api_client, user
    return make_auth

@pytest.fixture
def group(db):
    return Group.objects.create(name="TEST-GROUP")
