from http import HTTPStatus


def test_login_for_access_token(api_client, user):
    response = api_client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
        headers={'X-Tenant-Domain': user.tenant.domain},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_login_for_access_token_user_not_found(api_client, tenant):
    response = api_client.post(
        '/token',
        data={'username': 'test', 'password': 'test_password'},
        headers={'X-Tenant-Domain': tenant.domain},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_login_for_access_token_wrong_password(api_client, user):
    response = api_client.post(
        '/token',
        data={'username': user.email, 'password': 'wrong_password'},
        headers={'X-Tenant-Domain': user.tenant.domain},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}
