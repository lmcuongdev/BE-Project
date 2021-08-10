from marshmallow import Schema, fields


class ErrorSchema(Schema):
    error_message = fields.String(required=True)
    error_data = fields.Raw()
