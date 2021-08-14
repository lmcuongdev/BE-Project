from config.base import BaseConfig


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Cuong123@localhost/got_it'
