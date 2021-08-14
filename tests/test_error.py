from app import app, exception_handler
from errors import InternalServerError, NotFoundError


def test_not_found_error(client):
    response = client.get('/wrongurl')
    response_data = response.get_json()

    assert response.status_code == NotFoundError.status_code
    assert {'error_message'} == set(response_data.keys())
    assert response_data[
               'error_message'] == NotFoundError.default_error_message


def test_unhandled_exception():
    with app.test_request_context():
        resp = exception_handler(Exception())
        assert resp == InternalServerError().get_response()
