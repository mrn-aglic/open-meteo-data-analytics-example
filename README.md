# A celery workflow from API to analytics
This repo contains an example Celery workflow that:
- requests air quality data from open-meteo API
- transforms the data using Polars
- validates the data using Marshmallow
- stores the validated data to ClickHouse DB
- integrates Apache Superset for dashboards

To run the project, first create the `.env` file. You can
simply copy the `.env.example` file.

You can build the images by running:
```shell
make build
```
To run the project:
```shell
make run
```

A medium blog post is published to accompany this repo:
1. [Building a data pipeline from API to analytics dashboards.](https://medium.com/@MarinAgli1/building-a-data-pipeline-from-api-to-analytics-dashboards-8494df7e7aa7)


Weather data is collected from the open-meteo API:
https://open-meteo.com.

City data is collected from simple maps: 
https://simplemaps.com/data/world-cities.
