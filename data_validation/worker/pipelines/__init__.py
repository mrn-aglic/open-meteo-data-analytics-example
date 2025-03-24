from celery.utils.log import get_task_logger

from data_validation.celeryapp import app
from data_validation.worker.tasks.city import load_cities
from data_validation.worker.tasks.weather import get_weather_data

logger = get_task_logger(__name__)


@app.task(bind=True)
def result_map(self, ls: list[dict]):
    chain = self.request.chain

    logger.info(chain)

    return ls


@app.task
def city_weather_pipeline():
    return (load_cities.s() | get_weather_data.s()).apply_async()
