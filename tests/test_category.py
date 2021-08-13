from datetime import datetime

from config.config import General


def test_get_categories(client):
    response = client.get('/categories')
    response_data = response.get_json()

    assert response.status_code == 200

    # Check each key
    assert type(response_data['categories']) is list
    assert response_data['items_per_page'] == 10
    assert response_data['page'] == 1
    assert type(response_data['total_items']) is int

    # Check if dates is sorted ascending
    date_formatted = map(
        lambda category: datetime.strptime(
            category['created_at'],
            General.TIMESTAMP_FORMAT),
        response_data['categories']
    )
    dates = list(date_formatted)

    assert dates == sorted(dates)


def test_get_categories_with_page_parameters(client):
    params = {
        'items_per_page': 2,
        'page': 2,
    }
    response = client.get('/categories', query_string=params)
    response_data = response.get_json()

    assert response.status_code == 200

    # Check each key
    assert type(response_data['categories']) is list
    assert response_data['items_per_page'] == params['items_per_page']
    assert response_data['page'] == params['page']
    assert len(response_data['categories']) <= params['items_per_page']
    assert type(response_data['total_items']) is int

    # Check if dates is sorted ascending
    date_formatted = map(
        lambda category: datetime.strptime(
            category['created_at'],
            General.TIMESTAMP_FORMAT),
        response_data['categories']
    )
    dates = list(date_formatted)
    assert dates == sorted(dates)


def test_get_categories_with_all_parameters(client):
    params = {
        'items_per_page': 3,
        'page': 1,
        'keyword': 's',
        'sort_by': 'name',
        'sort_type': 'desc'
    }
    response = client.get('/categories', query_string=params)
    response_data = response.get_json()

    assert response.status_code == 200

    # Check each key
    assert type(response_data['categories']) is list
    assert response_data['items_per_page'] == params['items_per_page']
    assert response_data['page'] == params['page']
    assert len(response_data['categories']) <= params['items_per_page']
    assert type(response_data['total_items']) is int

    # Check if name contains the keyword provided
    name_contain_keyword = (
        params['keyword'].lower() in category['name'].lower()
        for category in response_data['categories']
    )
    assert all(name_contain_keyword)

    # Check sorting condition
    names = [category['name'] for category in response_data['categories']]
    assert names == sorted(names, reverse=True)


def test_get_categories_with_wrong_format(client):
    params = {
        'items_per_page': 3,
        'page': 'a string',
        'wrong_param': 'test'
    }
    response = client.get('/categories', query_string=params)
    response_data = response.get_json()

    assert response.status_code == 400
    assert {'error_message', 'error_data'} == response_data.keys()

    assert {'page', 'wrong_param'} == response_data['error_data'].keys()
