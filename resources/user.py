from flask_bcrypt import check_password_hash, generate_password_hash
from flask_restful import Resource
from marshmallow import ValidationError

from errors import NotFoundError, PermissionDeniedError, BadRequestError, \
    IncorrectCredentialError
from helpers.auth import create_access_token, jwt_required
from helpers.general import input_validated
from models.user import UserModel
from schemas.auth import AuthSchema, LoginRequestSchema
from schemas.user import UserSchema


class User(Resource):
    @jwt_required
    def get(self, user_id, auth_user):
        # Check token to see if this user is allowed to access this route
        if user_id != auth_user.id:
            raise PermissionDeniedError()

        # Check if this user_id exist
        user = UserModel.query.get(user_id)
        if not user:
            raise NotFoundError()

        # Get the user and return
        user_schema = UserSchema()
        data = user_schema.dump(user)

        return data


class UserRegister(Resource):
    @input_validated(AuthSchema())
    def post(self, valid_data):
        # Check if username existed
        if UserModel.has_username(valid_data['username']):
            raise BadRequestError(message='Username already existed.')

        hash_password = generate_password_hash(valid_data['password'])

        # Create new User
        user = UserModel(username=valid_data['username'],
                         password=hash_password)
        user.save()

        return {}


class UserLogin(Resource):
    @input_validated(LoginRequestSchema())
    def post(self, valid_data):
        # If the username or password doesn't match our database design,
        # then we don't need to query the database, instead return the
        # unauthorized response right away
        try:
            valid_data = AuthSchema().load(valid_data)
        except ValidationError:
            raise IncorrectCredentialError()

        username, password = valid_data['username'], valid_data['password']

        # If this user is found, create a new access token for it
        user = UserModel.find_by_username(username)
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(user_id=user.id)
        else:
            raise IncorrectCredentialError()

        return {'access_token': access_token}
