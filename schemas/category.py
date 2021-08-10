from marshmallow import Schema, fields, validate, post_load, post_dump

from schemas.base_query_parameter import QueryParameterSchema
from models.category import CategoryModel
from config.config import Config


class CategorySchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    created_at = fields.DateTime(format=Config.TIMESTAMP_FORMAT)


class CategoryQueryParameterSchema(QueryParameterSchema):
    sort_by = fields.String(load_default='created_at', validate=[
        validate.OneOf(['created_at', 'name'])
    ])

    @post_load
    def make_filterable(self, data, **kwargs):
        """Convert these fields to filterable objects that can be used in Query object"""

        # Get the Column object based on the requested 'sort_by' field
        sort_column = getattr(CategoryModel, data['sort_by'])

        # Since the 'sort_type' can only be 'asc' or 'desc', this will call asc() or desc() on the Column object
        # so that later it can be used as an argument in sqlalchemy.orm.query.Query.order_by method
        sort_type = getattr(sort_column, data['sort_type'])()

        # Create a filtering condition to be used in sqlalchemy.orm.query.Query.filter method,
        # we use LIKE operator to find all names containing the 'keyword'
        keyword_filter = CategoryModel.name.like(f"%{data['keyword']}%")

        data['sort_by'] = sort_column
        data['sort_type'] = sort_type
        data['keyword'] = keyword_filter

        return data
