from marshmallow import Schema, fields


class CountrySchema(Schema):
    name = fields.String(required=True)
    iso2_code = fields.String(required=True)
    iso3_code = fields.String(required=True)

    @staticmethod
    def get_columns():
        return set(CountrySchema().fields.keys())


class CitySchema(Schema):
    name = fields.String(required=True)
    country = fields.Nested(CountrySchema, required=True)
    lat = fields.Float(required=True)
    lng = fields.Float(required=True)
    ascii_code = fields.String(required=True)

    @staticmethod
    def get_columns():
        return set(CitySchema().fields.keys())
