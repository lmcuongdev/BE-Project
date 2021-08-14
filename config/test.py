from config.base import BaseConfig


class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Cuong123@localhost/test_got_it'
