import clickhouse_connect
import polars as pl
from celery.utils.log import get_task_logger

from data_validation.app.config import (
    CLICKHOUSE_DB,
    CLICKHOUSE_HOST,
    CLICKHOUSE_PASSWORD,
    CLICKHOUSE_PORT,
    CLICKHOUSE_USER,
)
from data_validation.celeryapp import app

logger = get_task_logger(__name__)

# ALTER TABLE air_quality MODIFY SETTING allow_experimental_replacing_merge_with_cleanup = 1;


@app.task
def optimise_table():
    client = clickhouse_connect.get_client(
        host=CLICKHOUSE_HOST,
        port=CLICKHOUSE_PORT,
        database="weather_data",
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
    )

    client.command("OPTIMIZE TABLE air_quality FINAL CLEANUP")
    logger.info("table optimised:> air_quality")


@app.task
def store_data_to_db(data: list[dict], table_name: str):
    logger.info(CLICKHOUSE_HOST)
    logger.info(CLICKHOUSE_DB)
    logger.info(CLICKHOUSE_PORT)
    logger.info(CLICKHOUSE_USER)
    logger.info(CLICKHOUSE_PASSWORD)

    client = clickhouse_connect.get_client(
        host=CLICKHOUSE_HOST,
        port=CLICKHOUSE_PORT,
        database="weather_data",
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
    )

    df = pl.from_dicts(data)
    df = df.with_columns(pl.col("date").str.strptime(pl.Datetime).alias("date"))

    client.insert_arrow(table=table_name, arrow_table=df.to_arrow())

    # client.command(f"OPTIMIZE {table_name} FINAL CLEANUP")

    count = client.query(f"SELECT COUNT(*) FROM {table_name} FINAL")

    logger.info(count.result_rows)
