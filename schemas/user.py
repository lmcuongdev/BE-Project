from marshmallow import Schema, fields

from config.config import General


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    created_at = fields.DateTime(format=General.TIMESTAMP_FORMAT)
