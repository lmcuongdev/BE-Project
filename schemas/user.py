from flask_bcrypt import generate_password_hash
from marshmallow import Schema, fields, validate, post_load

from config.config import General


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String(required=True,
                             validate=[
                                 validate.Length(max=20),
                                 validate.ContainsNoneOf(' ')
                             ])
    password = fields.String(required=True, validate=validate.Length(min=6, max=72))
    created_at = fields.DateTime(format=General.TIMESTAMP_FORMAT)

    @post_load
    def secure_user(self, data, **kwargs):
        data['password'] = generate_password_hash(data['password'])
        return data
