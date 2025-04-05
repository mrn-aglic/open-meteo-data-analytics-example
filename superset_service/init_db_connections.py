# pylint: disable=duplicate-code
import os

from superset import create_app, db

# Define the connection URI for ClickHouse
CLICKHOUSE_HOST = os.environ.get("CLICKHOUSE_HOST", "db")
CLICKHOUSE_PORT = "8123"
CLICKHOUSE_DB = os.environ["CLICKHOUSE_DB"]
CLICKHOUSE_USER = os.environ["CLICKHOUSE_USER"]
CLICKHOUSE_PASSWORD = os.environ["CLICKHOUSE_PASSWORD"]

clickhouse_uri = f"clickhousedb://{CLICKHOUSE_USER}:{CLICKHOUSE_PASSWORD}@{CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}/{CLICKHOUSE_DB}"

app = create_app()

with app.app_context():
    from superset.models.core import Database

    database_name = "Clickhouse analytics"

    existing = db.session.query(Database).filter_by(database_name=database_name).first()

    if existing:
        print(f"Database connection {existing} already exists")
    else:
        # Create the database object
        database = Database(database_name=database_name, sqlalchemy_uri=clickhouse_uri)

        # Add the database to the session
        db.session.add(database)
        db.session.commit()

        print(f"Added database connection to: {CLICKHOUSE_DB}")
