import itertools
from datetime import datetime, timedelta, timezone

import openmeteo_requests
import polars as pl
from celery.utils.log import get_task_logger
from openmeteo_sdk.Variable import Variable

from data_validation.app.config import AIR_QUALITY_PARAMS, OPEN_METEO_URLS
from data_validation.app.enums import OpenMeteoApiUrls
from data_validation.celeryapp import app
from data_validation.models.weather import WeatherSchema

logger = get_task_logger(__name__)


def _get_hourly_dataframe(weather_data) -> pl.DataFrame:
    hourly_response = weather_data.Hourly()

    start = datetime.fromtimestamp(hourly_response.Time(), timezone.utc)
    end = datetime.fromtimestamp(hourly_response.TimeEnd(), timezone.utc)
    freq = timedelta(seconds=hourly_response.Interval())

    hourly_variables = list(
        map(
            # lambda i: hourly_response.Variables(i),
            hourly_response.Variables,
            range(0, hourly_response.VariablesLength()),
        )
    )

    return pl.select(
        date=pl.datetime_range(start, end, freq, closed="left"),
        pm10=next(
            filter(lambda x: x.Variable() == Variable.pm10, hourly_variables)
        ).ValuesAsNumpy(),
        pm2_5=next(
            filter(lambda x: x.Variable() == Variable.pm2p5, hourly_variables)
        ).ValuesAsNumpy(),
        ozone=next(
            filter(lambda x: x.Variable() == Variable.ozone, hourly_variables)
        ).ValuesAsNumpy(),
        carbon_dioxide=next(
            filter(lambda x: x.Variable() == Variable.carbon_dioxide, hourly_variables)
        ).ValuesAsNumpy(),
        dust=next(
            filter(lambda x: x.Variable() == Variable.dust, hourly_variables)
        ).ValuesAsNumpy(),
        european_aqi=next(
            filter(lambda x: x.Variable() == Variable.european_aqi, hourly_variables)
        ).ValuesAsNumpy(),
        european_aqi_pm10=next(
            filter(
                lambda x: x.Variable() == Variable.european_aqi_pm10, hourly_variables
            )
        ).ValuesAsNumpy(),
        european_aqi_pm2_5=next(
            filter(
                lambda x: x.Variable() == Variable.european_aqi_pm2p5, hourly_variables
            )
        ).ValuesAsNumpy(),
        european_aqi_ozone=next(
            filter(
                lambda x: x.Variable() == Variable.european_aqi_ozone, hourly_variables
            )
        ).ValuesAsNumpy(),
    )


def process_single_weather_data(weather_data, city: dict) -> list[dict]:

    hourly_dataframe_pl = _get_hourly_dataframe(weather_data).with_columns(
        pl.col("date").dt.strftime("%Y-%m-%dT%H:%M:%S%z").alias("date")
    )

    data = {
        "city_name": city["name"],
        "country_iso2": city["country"]["iso2_code"],
        "latitude": city["lat"],
        "longitude": city["lng"],
        "elevation": weather_data.Elevation(),
    }

    city_basic_data = pl.DataFrame(data=data)

    df = city_basic_data.join(hourly_dataframe_pl, how="cross").sort(by=["date"])

    return df.to_dicts()


def process_response(response, cities: list[dict]) -> dict:
    weather_data = {
        (
            weather_data.Latitude(),
            weather_data.Longitude(),
        ): process_single_weather_data(weather_data, city)
        for weather_data, city in zip(response, cities)
    }

    return weather_data


@app.task
def get_weather_data(cities: list[dict]):
    params = {
        "hourly": AIR_QUALITY_PARAMS,
        "latitude": [city["lat"] for city in cities],
        "longitude": [city["lng"] for city in cities],
    }

    cities = [cities[0]]

    client = openmeteo_requests.Client()
    response = client.weather_api(
        url=OPEN_METEO_URLS[OpenMeteoApiUrls.AIR_QUALITY], params=params
    )

    data = process_response(response, cities)

    flattened_data = list(itertools.chain(*data.values()))
    WeatherSchema().validate_dicts(data=flattened_data)

    logger.info("validation passed")

    return flattened_data
