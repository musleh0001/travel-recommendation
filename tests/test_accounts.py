import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_valid_signup(api_client):
    url = reverse("sign-up")
    data = {"username": "test", "email": "test@email.com", "password": "mypasswd"}

    response = api_client.post(url, data, format="json")

    assert response.status_code == 201
    assert User.objects.count() == 1
    assert User.objects.first().username == "test"
    assert User.objects.first().email == "test@email.com"


@pytest.mark.django_db
def test_invalid_signup(api_client):
    url = reverse("sign-up")
    data = {
        "username": "test",
        "email": "test@email.com",
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == 400
    assert User.objects.count() == 0
