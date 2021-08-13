from flask_restful import Resource

from helpers.general import input_validated, make_query_filterable
from models.category import CategoryModel
from schemas.category import CategorySchema, CategoryQueryParameterSchema


class CategoryList(Resource):
    @input_validated(CategoryQueryParameterSchema(), query_param=True)
    def get(self, valid_data):
        # Reformat the query data to prepare for querying database
        params = make_query_filterable(valid_data, CategoryModel)

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
