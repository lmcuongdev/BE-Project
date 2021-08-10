from functools import wraps
from datetime import datetime
from jwt import encode, decode, get_unverified_header
from flask import request

from config.config import Config
from errors import UnauthorizedError, InvalidTokenError


def create_access_token(user_id):
    access_token = encode({
        'user_id': user_id,
        'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES
    }, Config.JWT_SECRET_KEY)

    return access_token


def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # check if the request contain the expected header
        if 'Authorization' not in request.headers:
            raise InvalidTokenError()

        # get the token
        data = request.headers['Authorization']
        token = str.replace(str(data), 'Bearer ', '')

        # decode the token to get the user_id stored in payload
        try:
            algo = get_unverified_header(token)['alg']
            auth_user_id = decode(token, Config.JWT_SECRET_KEY, algorithms=[algo])['user_id']
        except Exception as e:
            print(e.__traceback__)
            raise InvalidTokenError()
        return fn(auth_user_id=auth_user_id, *args, **kwargs)

    return wrapper
