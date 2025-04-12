import os
import numpy as np
import polars as pl
import requests_cache
import openmeteo_requests
from retry_requests import retry
from openmeteo_sdk.Variable import Variable
from datetime import datetime, timedelta, timezone


cache_session = requests_cache.CachedSession(".cache", expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
om = openmeteo_requests.Client(session=retry_session)
params = {
    "latitude": 23.7115253,
    "longitude": 90.4111451,
    "hourly": "temperature_2m",
    "forecast_days": 7,
}

responses = om.weather_api(os.getenv("WEATHER_API"), params=params)
response = responses[0]

hourly = response.Hourly()
hourly_time = range(hourly.Time(), hourly.TimeEnd(), hourly.Interval())
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

if __name__ == "__main__":
    from travel import utils

    result = utils.fetch_air_quality_data(lat=23.7115253, long=90.4111451)
    breakpoint()
