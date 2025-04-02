from celery.utils.log import get_task_logger

from data_validation.celeryapp import app
from data_validation.worker.tasks.city import load_cities
from data_validation.worker.tasks.database import store_data_to_db
from data_validation.worker.tasks.weather import get_weather_data

logger = get_task_logger(__name__)


@app.task
def city_weather_pipeline():
    return (load_cities.s() | get_weather_data.s()).apply_async()


@app.task
def store_to_db_pipeline(data: list[dict], table_name: str):
    return store_data_to_db.s(
        data=data,
        table_name=table_name,
    ).apply_async()
