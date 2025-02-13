from http import HTTPStatus

from fastapi.testclient import TestClient

from backend.main import app


def test_root_should_return_hello_world():
    client = TestClient(app)

    response = client.get('/')

    assert response.json() == {'Hello': 'World'}
    assert response.status_code == HTTPStatus.OK
