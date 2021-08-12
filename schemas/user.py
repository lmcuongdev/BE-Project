from marshmallow import Schema, fields, validate, post_load

from config.config import General


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String(required=True,
                             validate=[
                                 validate.Length(min=1, max=20),
                                 validate.ContainsNoneOf(' ', error="Must not contains any space")
                             ])
    password = fields.String(required=True, validate=validate.Length(min=6, max=72))
    created_at = fields.DateTime(format=General.TIMESTAMP_FORMAT)
