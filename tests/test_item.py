from datetime import datetime
from random import choice

import pytest
from marshmallow import ValidationError

from config.config import General
from errors import NotFoundError, InvalidTokenError, SchemaValidationError, \
    PermissionDeniedError
from schemas.item import ItemSchema

INVALID_FIELDS_TEST_DATA = [
    {
        'payload': {'name': '_'},
        'invalid_fields': ['description', 'category_id']
    },
    {
        'payload': {'description': '       ', 'category_id': 1},
        'invalid_fields': ['name', 'description']
    },
    {
        'payload': {'name': '_' * 201, 'description': '_', 'category_id': 1},
        'invalid_fields': ['name']
    },
    {
        'payload': {},
        'invalid_fields': ['name', 'description', 'category_id']
    },
    {
        'payload': {'name': '_' * 201, 'description': '_' * 2001,
                    'category_id': 99},
        'invalid_fields': ['name', 'description', 'category_id']
    },
]


def test_get_items_with_no_param(client, seed_items):
    response = client.get('/items')
    response_data = response.get_json()

    assert response.status_code == 200

    # Check each key
    assert type(response_data['items']) is list
    assert response_data['items_per_page'] == 10
    assert response_data['page'] == 1
    assert response_data['total_items'] == len(seed_items)

    # Check if dates is sorted ascending
    date_formatted = map(
        lambda item: datetime.strptime(
            item['created_at'],
            General.TIMESTAMP_FORMAT),
        response_data['items']
    )
    dates = list(date_formatted)
    assert dates == sorted(dates)


def test_get_items_with_page_param(client, seed_items):
    params = {
        'items_per_page': 2,
        'page': 2,
    }
    response = client.get('/items', query_string=params)
    response_data = response.get_json()

    assert response.status_code == 200

    # Check each key
    assert type(response_data['items']) is list
    assert response_data['items_per_page'] == params['items_per_page']
    assert response_data['page'] == params['page']
    assert response_data['total_items'] == len(seed_items)

    # Check if dates is sorted ascending
    date_formatted = map(
        lambda item: datetime.strptime(item['created_at'],
                                       General.TIMESTAMP_FORMAT),
        response_data['items']
    )
    dates = list(date_formatted)
    assert dates == sorted(dates)


def test_get_items_with_all_parameters(client):
    params = {
        'items_per_page': 3,
        'page': 1,
        'keyword': 'item',
        'sort_by': 'description',
        'sort_type': 'desc',
        'category_id': 1
    }
    response = client.get('/items', query_string=params)
    response_data = response.get_json()

    assert response.status_code == 200

    # Check each key
    assert type(response_data['items']) is list
    assert response_data['items_per_page'] == params['items_per_page']
    assert response_data['page'] == params['page']
    assert len(response_data['items']) <= params['items_per_page']
    assert type(response_data['total_items']) is int

    # Check if name contains the keyword provided
    name_contain_keyword = (
        params['keyword'].lower() in category['name'].lower()
        for category in response_data['items']
    )
    assert all(name_contain_keyword)

    # Check sorting condition
    names = [category[params['sort_by']] for category in
             response_data['items']]
    assert names == sorted(names, reverse=True)

    # Check category_id field
    category_id_match = (item['category_id'] == params['category_id'] for item
                         in response_data['items'])
    assert all(category_id_match)


def test_get_items_with_wrong_format(client):
    params = {
        'items_per_page': 3,
        'page': 'a string',
        'wrong_param': 'test'
    }
    response = client.get('/categories', query_string=params)
    response_data = response.get_json()

    assert response.status_code == 400
    assert {'error_message', 'error_data'} == set(response_data.keys())

    assert {'page', 'wrong_param'} == set(response_data['error_data'].keys())


def test_get_item_detail(client, seed_items):
    random_item = choice(seed_items)

    response = client.get(f"/items/{random_item['id']}")
    response_data = response.get_json()

    assert response.status_code == 200

    required_fields = random_item.keys() | {'created_at', 'updated_at'}
    assert set(required_fields) == set(response_data.keys())


def test_get_item_detail_not_found(client):
    response = client.get('/items/9999')
    response_data = response.get_json()

    assert response.status_code == NotFoundError.status_code
    assert response_data[
               'error_message'] == NotFoundError.default_error_message


def test_create_item_success(client, auth_user):
    headers = {
        'Authorization': f"Bearer {auth_user['access_token']}"
    }
    payload = {
        'name': 'test',
        'description': 'desc',
        'category_id': 1,
    }
    response = client.post('/items', json=payload, headers=headers)
    response_data = response.get_json()

    assert response.status_code == 200

    try:
        ItemSchema().load(response_data)
    except ValidationError:
        assert False
    else:
        assert True

    # Verify that the resource has been created
    next_response = client.get(f"/items/{response_data['id']}")
    next_response_data = next_response.get_json()

    assert next_response.status_code == 200
    assert next_response_data == response_data


def test_create_item_failed_invalid_token(client):
    headers = {
        'Authorization': 'Bearer'
    }
    payload = {
        'name': 'test',
        'description': 'desc',
        'category_id': 1,
    }
    response = client.post('/items', json=payload, headers=headers)
    response_data = response.get_json()

    assert response.status_code == InvalidTokenError.status_code
    assert {'error_message'} == set(response_data.keys())


@pytest.mark.parametrize('test_data', INVALID_FIELDS_TEST_DATA)
def test_create_item_failed_invalid_fields(client, auth_user, test_data):
    headers = {
        'Authorization': f"Bearer {auth_user['access_token']}"
    }
    response = client.post('/items', json=test_data['payload'],
                           headers=headers)
    response_data = response.get_json()

    assert response.status_code == SchemaValidationError.status_code
    assert {'error_message', 'error_data'} == set(response_data.keys())
    assert set(test_data['invalid_fields']) == set(
        response_data['error_data'].keys())


def test_create_item_failed_unknown_fields(client, auth_user):
    headers = {
        'Authorization': f"Bearer {auth_user['access_token']}"
    }
    payload = {
        'unknown_field': '_'
    }
    response = client.post('/items', json=payload, headers=headers)
    response_data = response.get_json()

    assert response.status_code == SchemaValidationError.status_code
    assert {'error_message', 'error_data'} == set(response_data.keys())
    assert 'unknown_field' in response_data['error_data']


def test_edit_item_success(client, seed_items, auth_user):
    """Edit item successfully when the authenticated user is the item's owner
    """

    # Based on the seed data, we assume the authenticated user own this item
    item = seed_items[0]

    headers = {
        'Authorization': f"Bearer {auth_user['access_token']}"
    }
    payload = {
        'name': 'new name',
        'description': 'new desc',
        'category_id': 1,
    }
    response = client.put(f"/items/{item['id']}", json=payload,
                          headers=headers)
    response_data = response.get_json()

    assert response.status_code == 200

    try:
        ItemSchema().load(response_data)
    except ValidationError:
        assert False
    else:
        assert True

    # Verify that the resource has been edited
    next_response = client.get(f"/items/{response_data['id']}")
    next_response_data = next_response.get_json()

    assert next_response.status_code == 200
    assert next_response_data == response_data


def test_edit_item_failed_permission_denied(client, seed_items, auth_user):
    """Edit item failed when the authenticated user is not the item's owner"""

    # Based on the seed data, we assume the authenticated user doesn't own this item
    item = seed_items[1]

    headers = {
        'Authorization': f"Bearer {auth_user['access_token']}"
    }
    payload = {
        'name': 'new name',
        'description': 'new desc',
        'category_id': 1,
    }
    response = client.put(f"/items/{item['id']}", json=payload,
                          headers=headers)
    response_data = response.get_json()

    assert response.status_code == PermissionDeniedError.status_code
    assert {'error_message'} == set(response_data.keys())
    assert response_data[
               'error_message'] == PermissionDeniedError.default_error_message


@pytest.mark.parametrize('test_data', INVALID_FIELDS_TEST_DATA)
def test_edit_item_failed_invalid_fields(client, seed_items, auth_user,
                                         test_data):
    """Edit item failed when the user is the item's owner but the provided data is invalid"""

    # Based on the seed data, we assume the authenticated user own this item
    item = seed_items[0]

    headers = {
        'Authorization': f"Bearer {auth_user['access_token']}"
    }
    response = client.put(f"/items/{item['id']}", json=test_data['payload'],
                          headers=headers)
    response_data = response.get_json()

    assert response.status_code == SchemaValidationError.status_code
    assert {'error_message', 'error_data'} == set(response_data.keys())
    assert set(test_data['invalid_fields']) == set(
        response_data['error_data'].keys())


def test_delete_item_success(client, seed_items, auth_user):
    """Delete item successfully when the authenticated user is the item's owner"""

    # Based on the seed data, we assume the authenticated user own this item
    item = seed_items[0]

    headers = {
        'Authorization': f"Bearer {auth_user['access_token']}"
    }
    response = client.delete(f"/items/{item['id']}", headers=headers)
    response_data = response.get_json()

    assert response.status_code == 200
    assert response_data == {}

    # Verify that the resource has been deleted
    next_response = client.get(f"/items/{item['id']}")

    assert next_response.status_code == NotFoundError.status_code


def test_delete_item_failed_permission_denied(client, seed_items, auth_user):
    """Delete item failed when the authenticated user is not the item's owner"""

    # Based on the seed data, we assume the authenticated user doesn't own this item
    item = seed_items[1]

    headers = {
        'Authorization': f"Bearer {auth_user['access_token']}"
    }
    response = client.delete(f"/items/{item['id']}", headers=headers)
    response_data = response.get_json()

    assert response.status_code == PermissionDeniedError.status_code
    assert {'error_message'} == set(response_data.keys())
    assert response_data[
               'error_message'] == PermissionDeniedError.default_error_message
