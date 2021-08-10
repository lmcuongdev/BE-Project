from flask_restful import Resource
from flask import request
from marshmallow import ValidationError

from models.category import CategoryModel
from schemas.category import CategorySchema, CategoryQueryParameterSchema
from errors import SchemaValidationError


class CategoryList(Resource):
    def get(self):
        # Check if query parameter is in valid format
        query_param_schema = CategoryQueryParameterSchema()
        try:
            params = query_param_schema.load(request.args)
        except ValidationError as e:
            raise SchemaValidationError(e.messages)

        # Find all the categories that match these query data
        category_page = CategoryModel.query \
            .filter(params['keyword']) \
            .order_by(params['sort_type']) \
            .paginate(page=params['page'],
                      per_page=params['items_per_page'],
                      error_out=False
                      )

        # Reformat the data before the response
        categories = CategorySchema(many=True).dump(category_page.items)

        return {
            'categories': categories,
            'items_per_page': params['items_per_page'],
            'page': params['page'],
            'total_items': category_page.total
        }
