import pytest

from errors import SchemaValidationError, BadRequestError, UnauthorizedError


def test_register_success(client):
    response = client.post('/auth/register', json={
        'username': 'a_unique_name',
        'password': 'password'
    })
    response_data = response.get_json()

    assert response.status_code == 200
    assert response_data == {}


def test_register_failed_missing_field(client):
    response = client.post('/auth/register', json={
        'username': 'sesaltme'
    })
    response_data = response.get_json()

    assert response.status_code == SchemaValidationError.status_code
    assert {'error_message', 'error_data'} == set(response_data.keys())
    assert {'password'} == set(response_data['error_data'].keys())


@pytest.mark.parametrize('invalid_username', ['has space', '_' * 21])
def test_register_failed_invalid_username(client, invalid_username):
    """Failed when username contains space or length>20"""
    response = client.post('/auth/register', json={
        'username': invalid_username,
        'password': 'abcsdadsa'
    })
    response_data = response.get_json()

    assert response.status_code == SchemaValidationError.status_code
    assert {'error_message', 'error_data'} == set(response_data.keys())
    assert {'username'} == set(response_data['error_data'].keys())


def test_register_failed_username_existed(client, seed_users):
    """Failed when username existed"""
    random_user = seed_users[0]
    response = client.post('/auth/register', json={
        'username': random_user['username'],
        'password': 'password'
    })
    response_data = response.get_json()

    assert response.status_code == BadRequestError.status_code
    assert {'error_message'} == set(response_data.keys())


@pytest.mark.parametrize('invalid_password', ['abc', '_' * 73])
def test_register_failed_invalid_password_length(client, invalid_password):
    """Failed when password length is less than 6 or more than 72"""
    response = client.post('/auth/register', json={
        'username': 'sesaltme',
        'password': invalid_password
    })
    response_data = response.get_json()

    assert response.status_code == SchemaValidationError.status_code
    assert {'error_message', 'error_data'} == response_data.keys()
    assert {'password'} == response_data['error_data'].keys()


def test_login_success(client, seed_users):
    random_user = seed_users[0]
    response = client.post('/auth/login', json={
        'username': random_user['username'],
        'password': 'password'
    })
    response_data = response.get_json()

    assert response.status_code == 200
    assert {'access_token'} == response_data.keys()


def test_login_failed_wrong_credential(client):
    response = client.post('/auth/login', json={
        'username': 'wrong_username',
        'password': 'wrong_password'
    })
    response_data = response.get_json()

    assert response.status_code == UnauthorizedError.status_code
    assert {'error_message'} == response_data.keys()


def test_login_missing_field(client):
    response = client.post('/auth/login', json={
        'username': 'admin'
    })
    response_data = response.get_json()

    assert response.status_code == SchemaValidationError.status_code
    assert {'error_message', 'error_data'} == response_data.keys()
    assert {'password'} == response_data['error_data'].keys()
