from marshmallow import Schema, fields, validate

from constants import General
from schemas.base_query_parameter import QueryParameterSchema


class CategorySchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    created_at = fields.DateTime(format=General.TIMESTAMP_FORMAT)


class CategoryQueryParameterSchema(QueryParameterSchema):
    sort_by = fields.String(load_default='created_at', validate=[
        validate.OneOf(['created_at', 'name'])
    ])
