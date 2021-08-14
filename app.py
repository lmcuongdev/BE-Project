import logging
from os import environ

from flask import Flask

from config import get_config
from constants import StatusCode
from database import db
from errors import Error, NotFoundError, InternalServerError
from resources import register_resources

app = Flask(__name__)

# get config based on environment
env = environ.get('ENVIRONMENT', 'dev')
app.config.from_object(get_config(env))

# config logging
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
