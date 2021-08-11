from flask import Flask
from flask_jwt_extended import JWTManager

from database import db
from config.config import Config
from resources import register_resources
from errors import Error, StatusCode, NotFoundError
import logging

app = Flask(__name__)

# configuring
app.config.from_object(Config)
logging.basicConfig(filename='logs.log', level=logging.DEBUG)

# setting up JWT
jwt = JWTManager(app)

# setting up SQLAlchemy
db.init_app(app)

# binding routes to its resources
register_resources(app)


@app.errorhandler(StatusCode.NOT_FOUND)
def not_found_handler(error):
    return NotFoundError().get_response()


@app.errorhandler(Error)
def error_handler(error):
    return error.get_response()


@app.errorhandler(Exception)
def exception_handler(error):
    logging.error(error, exc_info=True)
    return Error().get_response()
