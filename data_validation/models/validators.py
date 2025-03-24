from marshmallow import Schema, ValidationError


class SchemaValidator(Schema):
    def validate_dicts(self, data: list[dict]):
        validation_result = self.validate(data=data, many=True, partial=False)

        if validation_result:
            raise ValidationError(validation_result)
        return validation_result
