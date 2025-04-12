import pytest
import polars as pl
from datetime import date
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from travel.models import District


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="test", email="test@gmail.com", password="mypasswd"
    )


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def sample_districts():
    return [
        District.objects.create(
            division_id=1, name="Dhaka", bn_name="ঢাকা", lat=23.7115253, long=90.4111451
        ),
        District.objects.create(
            division_id=2,
            name="Faridpur",
            bn_name="ফরিদপুর",
            lat=23.6070822,
            long=89.8429406,
        ),
    ]


@pytest.fixture
def sample_weather_df():
    return pl.DataFrame(
        {
            "date": [str(date.today())],
            "temperature_2m": [25.0],
            "avg_temperature": [25.0],
        }
    )


@pytest.fixture
def sample_air_quality_df():
    return pl.DataFrame(
        {
            "date": [str(date.today())],
            "air_quality_pm2p5": [40.0],
            "avg_air_quality": [40.0],
        }
    )
