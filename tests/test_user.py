from errors import UnauthorizedError, PermissionDeniedError


def test_get_user_info_success(client, auth_user):
    headers = {'Authorization': f"Bearer {auth_user['access_token']}"}
    rv = client.get(f"/users/{auth_user['id']}", headers=headers)
    resp = rv.get_json()

    assert rv.status_code == 200
    assert {'id', 'username', 'created_at'} == set(resp.keys())


def test_get_user_info_failed_no_access_token(client, auth_user):
    rv = client.get(f"/users/{auth_user['id']}")
    resp = rv.get_json()

    assert rv.status_code == UnauthorizedError.status_code
    assert {'error_message'} == set(resp.keys())


def test_get_user_info_failed_invalid_token(client):
    headers = {'Authorization': 'Bearer an invalid token'}
    rv = client.get('/users/1', headers=headers)
    resp = rv.get_json()

    assert rv.status_code == UnauthorizedError.status_code
    assert {'error_message'} == set(resp.keys())


def test_get_user_info_failed_permission_denied(client, auth_user):
    """Authenticated user cannot access other user's information"""
    other_user_id = auth_user['id'] + 1

    headers = {'Authorization': f"Bearer {auth_user['access_token']}"}
    rv = client.get(f"/users/{other_user_id}", headers=headers)
    resp = rv.get_json()

    assert rv.status_code == PermissionDeniedError.status_code
    assert {'error_message'} == set(resp.keys())
