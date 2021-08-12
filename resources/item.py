from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from errors import SchemaValidationError, NotFoundError
from helpers.auth import jwt_required, item_owner_required
from models.item import ItemModel
from schemas.item import ItemSchema, ItemQueryParameterSchema


class ItemList(Resource):
    def get(self):
        # Check if query parameter is in valid format
        query_param_schema = ItemQueryParameterSchema()
        try:
            params = query_param_schema.load(request.args)
        except ValidationError as e:
            raise SchemaValidationError(e.messages)

        # Find all the items that match these query data
        item_page = ItemModel.query \
            .filter(params['keyword']) \
            .filter(params['category_id']) \
            .order_by(params['sort_type']) \
            .paginate(page=params['page'],
                      per_page=params['items_per_page'],
                      error_out=False
                      )

        # Reformat the data before the response
        items = ItemSchema(many=True).dump(item_page.items)

        return {
            'items': items,
            'items_per_page': params['items_per_page'],
            'page': params['page'],
            'total_items': item_page.total
        }

    @jwt_required
    def post(self, auth_user):
        #  Get the data sent from client
        payload = request.get_json()
        payload['user_id'] = auth_user.id

        # Validate input
        item_schema = ItemSchema(only=('name', 'description', 'user_id', 'category_id'))
        try:
            valid_data = item_schema.load(payload)
        except ValidationError as e:
            raise SchemaValidationError(error_messages=e.messages)

        # Create new item
        item = ItemModel(**valid_data)
        item.save()

        data = ItemSchema().dump(item)

        return data


class Item(Resource):
    def get(self, item_id):
        # Search fot this item in database
        item = ItemModel.query.get(item_id)
        if item is None:
            raise NotFoundError()

        data = ItemSchema().dump(item)

        return data

    @jwt_required
    @item_owner_required
    def put(self, item_id, auth_user, item):
        # Get request body and validate input
        payload = request.get_json()
        item_schema = ItemSchema(only=('name', 'description', 'category_id'))
        try:
            valid_data = item_schema.load(payload)
        except ValidationError as e:
            raise SchemaValidationError(error_messages=e.messages)

        # Update data
        item.update(**valid_data)
        item.save()

        data = ItemSchema().dump(item)

        return data

    @jwt_required
    @item_owner_required
    def delete(self, item_id, auth_user, item):
        item.delete()

        return {}
