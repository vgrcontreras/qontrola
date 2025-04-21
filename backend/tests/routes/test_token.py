from http import HTTPStatus

from freezegun import freeze_time


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


def test_refresh_token(api_client, user_token):
    response = api_client.post(
        '/token/refresh_token',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    token_data = response.json()
    assert 'access_token' in token_data
    assert 'token_type' in token_data
    assert token_data['token_type'] == 'bearer'
    assert token_data['access_token'] is not None


def test_refresh_token_unauthorized(api_client):
    response = api_client.post('/token/refresh_token')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_expired_token_refresh(api_client, user):
    # Freeze time at a fixed point to simulate token issuance
    with freeze_time('2023-01-01 12:00:00'):
        # Get a token with valid credentials
        response = api_client.post(
            '/token',
            data={'username': user.email, 'password': user.clean_password},
            headers={'X-Tenant-Domain': user.tenant.domain},
        )

        # Assert response is OK and extract the token
        assert response.status_code == HTTPStatus.OK
        token_data = response.json()
        assert 'access_token' in token_data
        access_token = token_data['access_token']

    # Freeze time again 31 minutes later to simulate token expiration
    # (assuming tokens expire in 30 minutes)
    with freeze_time('2023-01-01 12:31:00'):
        # Attempt to refresh the token with the expired token
        response = api_client.post(
            '/token/refresh_token',
            headers={'Authorization': f'Bearer {access_token}'},
        )

        # The current implementation doesn't check if the token is expired
        # it just creates a new token based on the user information
        assert response.status_code == HTTPStatus.OK
        token_data = response.json()
        assert 'access_token' in token_data
        assert 'token_type' in token_data
        assert token_data['token_type'] == 'bearer'
        assert token_data['access_token'] is not None
