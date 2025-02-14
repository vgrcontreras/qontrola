from http import HTTPStatus


def test_root_should_return_hello_world(client):
    response = client.get('/')

    assert response.json() == {'message': 'Olá Mundo!'}
    assert response.status_code == HTTPStatus.OK
