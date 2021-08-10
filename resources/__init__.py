from flask_restful import Api
from resources.user import User, UserLogin, UserRegister


def register_resources(app):
    api = Api(app)

    api.add_resource(User, '/users/<int:user_id>')
    api.add_resource(UserRegister, '/auth/register')
    api.add_resource(UserLogin, '/auth/login')
