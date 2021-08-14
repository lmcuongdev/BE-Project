from marshmallow import Schema, fields, validate


class AuthSchema(Schema):
    username = fields.String(required=True, validate=[
        validate.Length(min=1, max=20),
        validate.ContainsNoneOf(' ', error="Must not contains any space.")
    ])
    password = fields.String(required=True, validate=[
        validate.Length(min=6, max=72),
        validate.ContainsNoneOf(' ', error="Must not contains any space.")
    ])


class LoginRequestSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
