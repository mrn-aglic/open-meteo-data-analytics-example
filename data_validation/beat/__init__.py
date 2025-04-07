from celery.schedules import crontab
from celery.utils.log import get_task_logger

from data_validation.app import config
from data_validation.celeryapp import app
from data_validation.worker.pipelines import city_weather_pipeline

logger = get_task_logger(__name__)

if config.is_dev():
    import logging

    logging.basicConfig(level=logging.INFO)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        logger.info("SETUP PERIODIC TASK")

        sender.add_periodic_task(
            schedule=crontab(minute="0"),
            sig=city_weather_pipeline.s(),
            name="city_weather_pipeline",
        )

    except Exception as e:
        logger.error(f"An exception occurred: {e}")
