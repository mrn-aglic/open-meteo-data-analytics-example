-- init_weather_table.sql

CREATE TABLE IF NOT EXISTS weather_data.air_quality
(
    date DateTime,
    city_name String,
    country_iso2 String,
    latitude Float64,
    longitude Float64,
    elevation Float64,
    pm10 Float64,
    pm2_5 Float64,
    ozone Float64,
    carbon_dioxide Float64 DEFAULT NULL,
    dust Float64,
    european_aqi Float64,
    european_aqi_pm2_5 Float64,
    european_aqi_pm10 Float64,
    european_aqi_ozone Float64
) ENGINE = ReplacingMergeTree()
ORDER BY (date, city_name);
