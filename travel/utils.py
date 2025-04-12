import os
import polars as pl
import requests_cache
import openmeteo_requests
from retry_requests import retry
from openmeteo_sdk.Variable import Variable
from datetime import datetime, timedelta, timezone, date


# Setup client
cache_session = requests_cache.CachedSession(".cache", expire_after=timedelta(minutes=55))
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
om = openmeteo_requests.Client(session=retry_session)


def fetch_weather_data(
    lat: float, long: float, travel_date: date = None
) -> pl.DataFrame:
    params = {
        "latitude": lat,
        "longitude": long,
        "hourly": "temperature_2m",
    }

    if travel_date:
        params["start_date"] = travel_date
        params["end_date"] = travel_date
    else:
        params["forecast_days"] = 7

    responses = om.weather_api(os.getenv("WEATHER_API"), params=params)
    response = responses[0]

    hourly = response.Hourly()
    hourly_variables = list(
        map(lambda i: hourly.Variables(i), range(0, hourly.VariablesLength()))
    )

    hourly_temperature_2m = next(
        filter(
            lambda x: x.Variable() == Variable.temperature and x.Altitude() == 2,
            hourly_variables,
        )
    ).ValuesAsNumpy()

    start = datetime.fromtimestamp(hourly.Time(), timezone.utc)
    end = datetime.fromtimestamp(hourly.TimeEnd(), timezone.utc)
    freq = timedelta(seconds=hourly.Interval())

    df = pl.select(
        date=pl.datetime_range(start, end, freq, closed="left"),
        temperature_2m=hourly_temperature_2m,
    )

    # calculate average
    df_2pm = df.filter(pl.col("date").dt.hour() == 14)
    df = df.with_columns(
        pl.lit(df_2pm["temperature_2m"].mean()).alias("avg_temperature")
    )

    return df


def fetch_air_quality_data(
    lat: float, long: float, travel_date: date = None
) -> pl.DataFrame:
    params = {"latitude": lat, "longitude": long, "hourly": "pm2_5"}

    if travel_date:
        params["start_date"] = travel_date
        params["end_date"] = travel_date
    else:
        params["forecast_days"] = 7

    responses = om.weather_api(os.getenv("AIR_QUALITY_API"), params=params)
    response = responses[0]

    hourly = response.Hourly()
    hourly_variables = list(
        map(lambda i: hourly.Variables(i), range(0, hourly.VariablesLength()))
    )

    air_quality_pm2p5 = next(
        filter(lambda x: x.Variable() == Variable.pm2p5, hourly_variables)
    ).ValuesAsNumpy()

    start = datetime.fromtimestamp(hourly.Time(), timezone.utc)
    end = datetime.fromtimestamp(hourly.TimeEnd(), timezone.utc)
    freq = timedelta(seconds=hourly.Interval())

    df = pl.select(
        date=pl.datetime_range(start, end, freq, closed="left"),
        air_quality_pm2p5=air_quality_pm2p5,
    )

    # calculate avg
    filtered_df = df.filter(~pl.col("air_quality_pm2p5").is_nan())
    df = df.with_columns(
        pl.lit(filtered_df["air_quality_pm2p5"].mean()).alias("avg_air_quality")
    )

    return df
