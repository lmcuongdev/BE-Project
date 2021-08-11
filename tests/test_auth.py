import logging


def test_items(client):
    rv = client.get('/items')
    # print(type(rv.data))
    assert rv.status_code == 200
    # data = json.loads(rv.data)
    # assert isinstance(data['items'], list)
    # assert len(data['items']) > 100
