from datetime import datetime
from functools import wraps

from flask import request
from jwt import encode, decode, get_unverified_header, PyJWTError

from config.config import Config
from errors import InvalidTokenError, PermissionDeniedError
from models.user import UserModel


def create_access_token(user_id):
    """Create the access token and put user_id in the payload"""
    access_token = encode({
        'jti': user_id,
        'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES
    }, Config.JWT_SECRET_KEY)

    return access_token


def jwt_required(fn):
    """Validate the token in Authorization header to authenticate the user
    Then pass the authenticated user as a keyword argument if the token is
    valid
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Check if the request contain the expected header
        if 'Authorization' not in request.headers:
            raise InvalidTokenError()

        # Get the token
        data = request.headers['Authorization']
        if not data.startswith('Bearer '):
            raise InvalidTokenError()
        token = data.replace('Bearer ', '')

        # Decode the token to get the user_id stored in payload
        try:
            algo = get_unverified_header(token)['alg']
            payload = decode(token, Config.JWT_SECRET_KEY, algorithms=[algo])
            user_id = payload['jti']
        except PyJWTError:
            raise InvalidTokenError()

        # Get the authenticated user from database
        # Then pass it to the function being decorated
        auth_user = UserModel.query.get(user_id)

        return fn(auth_user=auth_user, *args, **kwargs)

    return wrapper


def item_owner_required(fn):
    """Check if the user is the owner of the an item
    If not, raise the PermissionDeniedError

    The function being decorated must pass 2 keyword arguments:
    1. auth_user: The authenticated user
    2. item: The item being checked

    This should be used after @jwt_required and @item_existed
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        item, auth_user = kwargs['item'], kwargs['auth_user']

        # If the user making the request is not the item's creator,
        # then this action is not allowed
        if item.user_id != auth_user.id:
            raise PermissionDeniedError()

        return fn(*args, **kwargs)

    return wrapper
