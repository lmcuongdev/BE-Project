from functools import wraps

from flask import request
from marshmallow import ValidationError

from errors import NotFoundError, SchemaValidationError
from models.category import CategoryModel
from models.item import ItemModel


def item_existed(fn):
    """
    The decorator to check if the item existed, then pass the item as a
    keyword argument
    It should receive item_id as keyword argument
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        item_id = kwargs['item_id']

        item = ItemModel.query.get(item_id)
        if item is None:
            raise NotFoundError()

        return fn(item=item, *args, **kwargs)

    return wrapper


def input_validated(schema):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            method = request.method

            if method in ('POST', 'PUT'):
                input_data = request.get_json()
            else:
                input_data = request.args

            try:
                valid_data = schema.load(input_data)
            except ValidationError as e:
                raise SchemaValidationError(error_messages=e.messages)

            return fn(valid_data=valid_data, *args, **kwargs)

        return wrapper

    return decorator


def has_related_category(fn):
    """Check if the requested category_id existed in database
    This should be used after @input_validated to receive valid_data as
    keyword argument
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        valid_data = kwargs['valid_data']

        category = CategoryModel.query.get(valid_data['category_id'])
        if category is None:
            error_messages = {'category_id': ['The category_id is invalid']}
            raise SchemaValidationError(error_messages)
        return fn(*args, **kwargs)

    return wrapper


def make_query_filterable(query_params, model):
    """Convert these fields to filterable objects that can be used in Query
    object
    """
    data = query_params.copy()

    # Get the Column object based on the requested 'sort_by' field
    sort_column = getattr(model, data['sort_by'])

    # Since the 'sort_type' can only be 'asc' or 'desc', this will call asc()
    # or desc() on the Column object so that later it can be used as an
    # argument in sqlalchemy.orm.query.Query.order_by method
    sort_type = getattr(sort_column, data['sort_type'])()

    # Create a filtering condition to be used in
    # sqlalchemy.orm.query.Query.filter method, we use LIKE operator to find
    # all names containing the 'keyword'
    keyword_filter = model.name.like(f"%{data['keyword']}%")

    data['sort_by'] = sort_column
    data['sort_type'] = sort_type
    data['keyword'] = keyword_filter

    return data
