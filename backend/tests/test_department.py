from http import HTTPStatus


def test_create_department(client):
    response = client.post('/departments/', json={'name': 'test_department'})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'name': 'test_department'}
