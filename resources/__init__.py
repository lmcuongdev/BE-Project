from flask_restful import Api

from resources.category import CategoryList
from resources.item import Item, ItemList
from resources.user import User, UserLogin, UserRegister


def register_resources(app):
    api = Api(app)

    # User related resources
    api.add_resource(User, '/users/<int:user_id>')
    api.add_resource(UserRegister, '/auth/register')
    api.add_resource(UserLogin, '/auth/login')

    # Category related resources
    api.add_resource(CategoryList, '/categories')

    # Item related resources
    api.add_resource(ItemList, '/items')
    api.add_resource(Item, '/items/<int:item_id>')
