from config.development import DevelopmentConfig
from config.production import ProductionConfig
from config.staging import StagingConfig


def get_config(env='dev'):
    if env == 'dev':
        return DevelopmentConfig
    if env == 'stg':
        return StagingConfig
    if env == 'prod':
        return ProductionConfig
