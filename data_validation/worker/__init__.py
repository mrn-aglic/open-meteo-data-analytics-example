from celery.utils.log import get_task_logger

from data_validation.app import config
from data_validation.celeryapp import app
from data_validation.worker import signals

logger = get_task_logger(__name__)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        if config.is_scheduler():
            return

    except Exception as e:
        logger.error(f"An exception occurred: {e}")
