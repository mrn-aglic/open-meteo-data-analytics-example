from marshmallow import fields

from data_validation.models.validators import SchemaValidator


class AirQualitySchema(SchemaValidator):
    date = fields.DateTime(required=True, format="%Y-%m-%dT%H:%M:%S%z")
    city_name = fields.String(required=True)
    country_iso2 = fields.String(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    elevation = fields.Float(required=True)
    pm10 = fields.Float(required=True)
    pm2_5 = fields.Float(required=True)
    ozone = fields.Float(required=True)
    carbon_dioxide = fields.Float(required=True, allow_nan=True)
    dust = fields.Float(required=True)
    european_aqi = fields.Float(required=True)
    european_aqi_pm2_5 = fields.Float(required=True)
    european_aqi_pm10 = fields.Float(required=True)
    european_aqi_ozone = fields.Float(required=True)

    @staticmethod
    def get_columns():
        return set(AirQualitySchema().fields.keys())
