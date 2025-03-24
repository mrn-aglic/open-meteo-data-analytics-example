import polars as pl

from data_validation.app.config import CITIES_TUPLE
from data_validation.celeryapp import app
from data_validation.models.city import CitySchema, CountrySchema


def get_valid_columns():
    city_columns = CitySchema.get_columns()
    country_columns = CountrySchema.get_columns()

    return set(city_columns) | set(country_columns)


def transform_dataframe(df: pl.DataFrame) -> pl.DataFrame:
    city_cols = [col for col in CitySchema.get_columns() if col != "country"]
    country_cols = list(CountrySchema.get_columns())

    cols = city_cols + [
        pl.struct(country_cols).alias("country"),
    ]

    return df.select(cols)
    # .with_columns(pl.lit(1).alias("dummy_column")))


@app.task
def load_cities():
    df = pl.read_csv("data/worldcities.csv", infer_schema_length=100000)

    df = df.rename(
        mapping={
            "city": "name",
            "city_ascii": "ascii_code",
            "iso2": "iso2_code",
            "iso3": "iso3_code",
        }
    )

    columns = ",".join(get_valid_columns())
    # struct or json_object are not currently supported
    df = df.sql(
        f"""
            SELECT
                {columns},
            FROM cities
            WHERE LOWER(name) + LOWER(country) IN {tuple(city + country for city, country in CITIES_TUPLE)}
        """,
        table_name="cities",
    )

    # df = df.select(list(get_valid_columns())).filter(
    #     pl.col("name").str.to_lowercase().is_in([city[0] for city in CITIES_TUPLE]) &
    #     pl.col("country").str.to_lowercase().is_in([city[1] for city in CITIES_TUPLE])
    # )

    df = transform_dataframe(df)

    result = df.to_dicts()

    CitySchema().validate_dicts(result)

    return result
