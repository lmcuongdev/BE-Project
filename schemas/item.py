from marshmallow import Schema, fields, validate, post_load, validates, ValidationError

from schemas.base_query_parameter import QueryParameterSchema
from models.item import ItemModel
from models.category import CategoryModel
from config.config import Config


class ItemSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    description = fields.String(required=True)
    user_id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)
    created_at = fields.DateTime(format=Config.TIMESTAMP_FORMAT)
    updated_at = fields.DateTime(format=Config.TIMESTAMP_FORMAT)

    @validates('category_id')
    def validate_category_id(self, category_id):
        category = CategoryModel.query.get(category_id)
        if category is None:
            raise ValidationError('The category id is invalid')


class ItemQueryParameterSchema(QueryParameterSchema):
    sort_by = fields.String(load_default='created_at', validate=[
        validate.OneOf(['created_at', 'updated_at', 'name', 'description'])
    ])
    category_id = fields.Integer()

    @post_load
    def make_filterable(self, data, **kwargs):
        """Convert these fields to filterable objects that can be used in Query object"""

        # Get the Column object based on the requested 'sort_by' field
        sort_column = getattr(ItemModel, data['sort_by'])

        # Since the 'sort_type' can only be 'asc' or 'desc', this will call asc() or desc() on the Column object
        # so that later it can be used as an argument in sqlalchemy.orm.query.Query.order_by method
        sort_type = getattr(sort_column, data['sort_type'])()

        # Create a filtering condition to be used in sqlalchemy.orm.query.Query.filter method,
        # we use LIKE operator to find all names containing the 'keyword'
        keyword_filter = ItemModel.name.like(f"%{data['keyword']}%")

        if 'category_id' in data:
            # If the field is provided, create a filtering condition using its column
            data['category_id'] = ItemModel.category_id == data['category_id']
        else:
            # Else set the field to True, so the query will ignore the condition
            data['category_id'] = True

        data['sort_by'] = sort_column
        data['sort_type'] = sort_type
        data['keyword'] = keyword_filter

        return data
