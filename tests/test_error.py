from errors import NotFoundError


def test_not_found_error(client):
    response = client.get('/wrongurl')
    response_data = response.get_json()

    assert response.status_code == NotFoundError.status_code
    assert {'error_message'} == set(response_data.keys())
    assert response_data['error_message'] == NotFoundError.default_error_message
