from os import environ
from datetime import timedelta


class Config:
    # Database connection
    SQLALCHEMY_DATABASE_URI = environ.get('MYSQL_URL')

    # SQLAlchemy config
    SQLALCHEMY_TRACK_MODIFICATIONS = bool(environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False))
    SQLALCHEMY_ECHO = bool(int(environ.get('SQLALCHEMY_ECHO', False)))

    # JWT
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY', '')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=float(
        environ.get('JWT_TOKEN_EXPIRES', 24 * 60 * 60)
    ))


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = False

    # Database connection
    SQLALCHEMY_DATABASE_URI = environ.get('TEST_MYSQL_URL')


class General:
    TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
