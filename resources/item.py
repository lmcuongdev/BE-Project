from flask_restful import Resource

from helpers.auth import jwt_required, item_owner_required
from helpers.general import item_existed, input_validated, \
    make_query_filterable, has_related_category
from models.item import ItemModel
from schemas.item import ItemSchema, ItemUpdateSchema, ItemCreateSchema, \
    ItemQueryParameterSchema


class ItemList(Resource):
    @input_validated(ItemQueryParameterSchema())
    def get(self, valid_data):
        # Reformat the query data to prepare for querying database
        params = make_query_filterable(valid_data, ItemModel)

        # If the field is provided, create a condition using its column,
        # if not, set the field to True, so the query will ignore the condition
        if 'category_id' in params:
            params['category_id'] = \
                ItemModel.category_id == params['category_id']
        else:
            params['category_id'] = True

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
    @input_validated(ItemCreateSchema())
    @has_related_category
    def post(self, valid_data, auth_user):
        # Create new item
        item = ItemModel(user_id=auth_user.id, **valid_data)
        item.save()

        data = ItemSchema().dump(item)

        return data


class Item(Resource):
    @item_existed
    def get(self, item, **_kwargs):
        # Search fot this item in database
        data = ItemSchema().dump(item)

        return data

    @jwt_required
    @item_existed
    @item_owner_required
    @input_validated(ItemUpdateSchema())
    @has_related_category
    def put(self, item, valid_data, **_kwargs):
        # Update data
        item.update(**valid_data)
        item.save()

        data = ItemSchema().dump(item)

        return data

    @jwt_required
    @item_existed
    @item_owner_required
    def delete(self, item, **_kwargs):
        item.delete()

        return {}
