from marshmallow import Schema, fields, validate


class QueryParameterSchema(Schema):
    items_per_page = fields.Integer(load_default=10, validate=[
        validate.Range(min=1, max=100)
    ])
    page = fields.Integer(load_default=1, validate=[
        validate.Range(min=1)
    ])
    sort_by = fields.String(load_default='created_at')
    sort_type = fields.String(load_default='asc', validate=[
        validate.OneOf(['asc', 'desc'])
    ])
    keyword = fields.String(load_default='')
