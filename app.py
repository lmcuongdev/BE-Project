from flask import Flask
from flask_jwt_extended import JWTManager

from database import db
from config.config import Config
from resources import register_resources
from errors import Error, StatusCode, NotFoundError

app = Flask(__name__)

# configuring
app.config.from_object(Config)

# setting up JWT
jwt = JWTManager(app)

# setting up SQLAlchemy
db.init_app(app)

# binding routes to its resources
register_resources(app)


@app.errorhandler(StatusCode.NOT_FOUND)
def not_found_handler():
    return NotFoundError().get_response()


@app.errorhandler(Error)
def error_handler(error):
    return error.get_response()
