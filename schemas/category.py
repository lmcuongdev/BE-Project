from marshmallow import Schema, fields, validate, post_load

from schemas.base_query_parameter import QueryParameterSchema
from models.category import CategoryModel


class CategorySchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class CategoryQueryParameterSchema(QueryParameterSchema):
    sort_by = fields.String(load_default='created_at', validate=[
        validate.OneOf(['created_at', 'name'])
    ])

    @post_load
    def get_column(self, data, **kwargs):
        sort_column = getattr(CategoryModel, data['sort_by'])
        sort_type = getattr(sort_column, data['sort_type'])()
        keyword_filter = CategoryModel.name.like(f"%{data['keyword']}%")

        data['sort_by'] = sort_column
        data['sort_type'] = sort_type
        data['keyword'] = keyword_filter

        return data
