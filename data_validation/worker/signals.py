from celery.signals import task_postrun

from data_validation.worker.pipelines import store_to_db_pipeline
from data_validation.worker.tasks.weather import get_weather_data


@task_postrun.connect(sender=get_weather_data)
def trigger_db_store(retval, state, **_):
    if not retval:
        print("No return value from task")
        return

    if state != "SUCCESS":
        print("Task not in success state")
        return

    if retval.get("data") and retval.get("table_name"):
        store_to_db_pipeline.s(
            data=retval.get("data"), table_name=retval.get("table_name")
        ).apply_async()
