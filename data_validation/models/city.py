from marshmallow import fields

from data_validation.models.validators import SchemaValidator


class CountrySchema(SchemaValidator):
    name = fields.String(required=True)
    iso2_code = fields.String(required=True)
    iso3_code = fields.String(required=True)

    @staticmethod
    def get_columns():
        return set(CountrySchema().fields.keys())


class CitySchema(SchemaValidator):
    name = fields.String(required=True)
    country = fields.Nested(CountrySchema, required=True)
    lat = fields.Float(required=True)
    lng = fields.Float(required=True)
    ascii_code = fields.String(required=True)

    @staticmethod
    def get_columns():
        return set(CitySchema().fields.keys())
