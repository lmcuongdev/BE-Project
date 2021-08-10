from marshmallow import Schema, fields


class AccessTokenSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
