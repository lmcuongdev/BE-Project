from os import environ
from datetime import timedelta


class Config:
    # Database connection
    SQLALCHEMY_DATABASE_URI = environ.get('MYSQL_URL')

    # JWT
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY', '')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=float(
        environ.get('JWT_TOKEN_EXPIRES', 24 * 60 * 60)
    ))
    JWT_ERROR_MESSAGE_KEY = environ.get('MESSAGE_KEY', 'error_message')
    JWT_HEADER_TYPE = environ.get('JWT_HEADER_TYPE', 'Bearer')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
