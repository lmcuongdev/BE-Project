from flask import request
from flask_bcrypt import check_password_hash
from flask_restful import Resource
from marshmallow import ValidationError

from errors import NotFoundError, PermissionDeniedError, UnauthorizedError, SchemaValidationError, \
    IncorrectCredentialError
from helpers.auth import create_access_token, jwt_required
from models.user import UserModel
from schemas.auth import AccessTokenSchema
from schemas.user import UserSchema


class User(Resource):
    @jwt_required
    def get(self, user_id, auth_user_id):
        # check token to see if this user is allowed to access this route
        if user_id != auth_user_id:
            raise PermissionDeniedError()

        # check if this user_id exist
        user = UserModel.query.get(user_id)
        if not user:
            raise NotFoundError()

        # get the user and return
        user_schema = UserSchema(only=('id', 'username', 'created_at'))
        data = user_schema.dump(user)

        return data


class UserRegister(Resource):
    def post(self):
        #  validate input
        user_schema = UserSchema(only=('username', 'password'))
        try:
            valid_data = user_schema.load(request.get_json())
        except ValidationError as e:
            raise SchemaValidationError(error_messages=e.messages)

        # check if username existed
        if UserModel.has_username(valid_data['username']):
            # error_data = {'username': 'Username already existed'}
            raise UnauthorizedError(message='Username already existed.')

        # create new User
        user = UserModel(**valid_data)
        user.save()

        return {}, 200


class UserLogin(Resource):
    def post(self):
        schema = AccessTokenSchema()
        #  validate input
        try:
            valid_data = schema.load(request.get_json())
        except ValidationError as e:
            raise SchemaValidationError(error_messages=e.messages)

        username, password = valid_data['username'], valid_data['password']

        # if this user is found, create a new access token for it
        user = UserModel.find_by_username(username)
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(user_id=user.id)
        else:
            raise IncorrectCredentialError()

        return {'access_token': access_token}
