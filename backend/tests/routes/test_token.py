from http import HTTPStatus


def test_login_for_access_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_login_for_access_token_user_not_found(client):
    response = client.post(
        '/token', data={'username': 'test', 'password': 'test_password'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_login_for_access_token_wrong_password(client, user):
    response = client.post(
        '/token', data={'username': user.email, 'password': 'wrong_password'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}
