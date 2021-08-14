from datetime import timedelta


class BaseConfig:
    TESTING = False

    # Database connection
    SQLALCHEMY_DATABASE_URI = ''

    # SQLAlchemy config
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # JWT
    JWT_SECRET_KEY = 'secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=float(24 * 60 * 60))
