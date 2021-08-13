from marshmallow import Schema, fields, validate, pre_load, validates, ValidationError

from config.config import General
from models.category import CategoryModel
from schemas.base_query_parameter import QueryParameterSchema


class ItemSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    user_id = fields.Integer()
    category_id = fields.Integer()
    created_at = fields.DateTime(format=General.TIMESTAMP_FORMAT)
    updated_at = fields.DateTime(format=General.TIMESTAMP_FORMAT)


class UpdateItemSchema(Schema):
    name = fields.String(required=True,
                         validate=[
                             validate.Length(min=1, max=200)
                         ])
    description = fields.String(required=True,
                                validate=[
                                    validate.Length(min=1, max=2000)
                                ])
    category_id = fields.Integer(required=True)

    @validates('category_id')
    def validate_category_id(self, category_id):
        category = CategoryModel.query.get(category_id)
        if category is None:
            raise ValidationError('The category id is invalid')

    @pre_load
    def trim_data(self, data, **_kwargs):
        keys = ['name', 'description']
        trimmed_data = {key: data[key].strip() for key in keys if key in data}

        data.update(trimmed_data)

        return data


class ItemQueryParameterSchema(QueryParameterSchema):
    sort_by = fields.String(load_default='created_at', validate=[
        validate.OneOf(['created_at', 'updated_at', 'name', 'description'])
    ])
    category_id = fields.Integer()
