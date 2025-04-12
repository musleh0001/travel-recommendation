import pytest
import polars as pl
from datetime import date
from unittest.mock import patch
from django.urls import reverse


@pytest.mark.django_db
@patch("travel.utils.fetch_weather_data")
@patch("travel.utils.fetch_air_quality_data")
def test_top_districts_view(
    mock_air,
    mock_weather,
    auth_client,
    sample_districts,
    sample_weather_df,
    sample_air_quality_df,
):
    mock_weather.return_value = sample_weather_df
    mock_air.return_value = sample_air_quality_df

    url = reverse("top-districts")
    response = auth_client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert "district" in response.data[0]


@pytest.mark.django_db
@patch("travel.utils.fetch_weather_data")
@patch("travel.utils.fetch_air_quality_data")
def test_recommend_travel_view_recommended(
    mock_air,
    mock_weather,
    auth_client,
    sample_districts,
    sample_weather_df,
    sample_air_quality_df,
):
    mock_weather.side_effect = [
        pl.DataFrame({"avg_temperature": [30.0]}),  # current temp
        pl.DataFrame({"avg_temperature": [25.0]}),  # dest temp
    ]
    mock_air.side_effect = [
        pl.DataFrame({"avg_air_quality": [80.0]}),  # current air
        pl.DataFrame({"avg_air_quality": [40.0]}),  # dest air
    ]

    url = reverse("recommend-travel")
    payload = {
        "latitude": 23.6070822,
        "longitude": 89.8429406,
        "destination_district": "Dhaka",
        "travel_date": str(date.today()),
    }

    response = auth_client.post(url, data=payload, format="json")

    assert response.status_code == 200
    assert response.data["recommendation"] == "Recommended"


@pytest.mark.django_db
@patch("travel.utils.fetch_weather_data")
@patch("travel.utils.fetch_air_quality_data")
def test_recommend_travel_view_not_recommended(
    mock_air,
    mock_weather,
    auth_client,
    sample_districts,
    sample_weather_df,
    sample_air_quality_df,
):
    mock_weather.side_effect = [
        pl.DataFrame({"avg_temperature": [20.0]}),  # current temp
        pl.DataFrame({"avg_temperature": [25.0]}),  # dest temp
    ]
    mock_air.side_effect = [
        pl.DataFrame({"avg_air_quality": [30.0]}),  # current air
        pl.DataFrame({"avg_air_quality": [60.0]}),  # dest air
    ]

    url = reverse("recommend-travel")
    payload = {
        "latitude": 23.6070822,
        "longitude": 89.8429406,
        "destination_district": "Dhaka",
        "travel_date": str(date.today()),
    }

    response = auth_client.post(url, data=payload, format="json")

    assert response.status_code == 200
    assert response.data["recommendation"] == "Not Recommended"


@pytest.mark.django_db
def test_recommend_travel_invalid_district(auth_client):
    url = reverse("recommend-travel")
    payload = {
        "latitude": 10.0,
        "longitude": 20.0,
        "destination_district": "UnknownCity",
        "travel_date": str(date.today()),
    }

    response = auth_client.post(url, data=payload, format="json")

    assert response.status_code == 200
    assert response.data["status"] == "failed"
    assert "not found" in response.data["message"].lower()
