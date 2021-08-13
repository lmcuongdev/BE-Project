from datetime import timedelta


class Config:
    TESTING = False

    # Database connection
    SQLALCHEMY_DATABASE_URI = ''

    # SQLAlchemy config
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # JWT
    JWT_SECRET_KEY = 'secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=float(24 * 60 * 60))


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Cuong123@localhost/got_it'


class StagingConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Cuong123@localhost/test_got_it'


class General:
    TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
