# menu/tests/conftest.py

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(api_client):
    username = "testuser"
    password = "testpass"
    api_client.post(
        "/api/register/",
        data={"username": username, "password": password},
        format="json",
    )
    response = api_client.post(
        "/api/token/",
        data={"username": username, "password": password},
        format="json",
    )
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client, username
