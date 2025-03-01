from celery.utils.log import get_task_logger

from data_validation.app import config
from data_validation.celeryapp import app
from data_validation.worker.tasks.city import load_cities

logger = get_task_logger(__name__)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        if config.is_scheduler():
            return

        load_cities.s().apply_async(countdown=10)

    except Exception as e:
        logger.error(f"An exception occurred: {e}")
