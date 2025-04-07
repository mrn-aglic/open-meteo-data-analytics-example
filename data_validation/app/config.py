import os
from os import environ

from .enums import OpenMeteoApiUrls

ENVIRONMENT = environ.get("ENVIRONMENT", "").upper()
DEV_NAME = "DEV"

if ENVIRONMENT not in ("PROD", DEV_NAME):
    raise ValueError("Please set the environment variable to either DEV or PROD")


def is_scheduler():
    return environ.get("instance", "").upper() == "SCHEDULER"


def is_dev():
    return ENVIRONMENT == DEV_NAME


CITIES_LIST = [
    {"city": "New York", "country": "United States"},
    {"city": "London", "country": "United Kingdom"},
    {"city": "Tokyo", "country": "Japan"},
    {"city": "Paris", "country": "France"},
    {"city": "Sydney", "country": "Australia"},
    {"city": "Berlin", "country": "Germany"},
    {"city": "Toronto", "country": "Canada"},
    {"city": "São Paulo", "country": "Brazil"},
    {"city": "Dubai", "country": "United Arab Emirates"},
    {"city": "Cape Town", "country": "South Africa"},
    {"city": "Mumbai", "country": "India"},
    {"city": "Seoul", "country": "Korea, South"},
    {"city": "Moscow", "country": "Russia"},
    {"city": "Bangkok", "country": "Thailand"},
    {"city": "Mexico City", "country": "Mexico"},
    {"city": "Istanbul", "country": "Turkey"},
    {"city": "Singapore", "country": "Singapore"},
    {"city": "Buenos Aires", "country": "Argentina"},
    {"city": "Rome", "country": "Italy"},
    {"city": "Cairo", "country": "Egypt"},
]

print(f"CITIES_LIST: len(CITIES_LIST): {len(CITIES_LIST)}")

CITIES_TUPLE = [(city["city"].lower(), city["country"].lower()) for city in CITIES_LIST]

OPEN_METEO_URLS = {
    OpenMeteoApiUrls.AIR_QUALITY: "https://air-quality-api.open-meteo.com/v1/air-quality"
}

AIR_QUALITY_PARAMS = [
    "pm10",
    "pm2_5",
    "ozone",
    "carbon_dioxide",
    "dust",
    "european_aqi",
    "european_aqi_pm2_5",
    "european_aqi_pm10",
    "european_aqi_ozone",
]

CLICKHOUSE_HOST = os.environ.get("CLICKHOUSE_HOST", "db")
CLICKHOUSE_PORT = "8123"
CLICKHOUSE_DB = os.environ["CLICKHOUSE_DB"]
CLICKHOUSE_USER = os.environ["CLICKHOUSE_USER"]
CLICKHOUSE_PASSWORD = os.environ["CLICKHOUSE_PASSWORD"]
