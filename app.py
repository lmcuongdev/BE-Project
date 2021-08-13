import logging
from os import environ

from flask import Flask

from config.config import DevelopmentConfig, ProductionConfig, StagingConfig
from database import db
from errors import Error, StatusCode, NotFoundError, InternalServerError
from resources import register_resources

app = Flask(__name__)

env = environ.get('ENVIRONMENT', 'dev')
if env == 'dev':
    app.config.from_object(DevelopmentConfig)
elif env == 'prod':
    app.config.from_object(ProductionConfig)
elif env == 'stg':
    app.config.from_object(StagingConfig)

# configuring
logging.basicConfig(filename='logs.log',
                    format=f'[%(asctime)s] %(levelname)s: %(message)s'
                    )

# setting up SQLAlchemy
db.init_app(app)

# binding routes to its resources
register_resources(app)


@app.errorhandler(StatusCode.NOT_FOUND)
def not_found_handler(error):
    app.log_exception(error)
    return NotFoundError().get_response()


@app.errorhandler(Error)
def error_handler(error):
    app.log_exception(error)
    return error.get_response()


@app.errorhandler(Exception)
def exception_handler(error):
    app.log_exception(error)
    return InternalServerError().get_response()
