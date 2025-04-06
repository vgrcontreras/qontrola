from http import HTTPStatus

import pytest

# Mark all tests in this module as asyncio tests
pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_get_user_me(api_client, user, user_token):
    """Test getting current user info"""
    response = api_client.get(
        '/users/me',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['email'] == user.email
    assert data['full_name'] == user.full_name
    assert str(data['id']) == str(user.id)
    assert data['is_active'] is True
    assert str(data['tenant_id']) == str(user.tenant_id)


@pytest.mark.asyncio
async def test_change_password_me(api_client, user, user_token):
    """Test changing own password"""
    response = api_client.patch(
        '/users/me/change-password',
        json={
            'password': 'new_password',
            'password_confirmation': 'new_password',
        },
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['message'] == 'Password has been changed!'

    # Verify login with new password works
    login_response = api_client.post(
        '/token',
        data={'username': user.email, 'password': 'new_password'},
        headers={'X-Tenant-Domain': user.tenant.domain},
    )
    assert login_response.status_code == HTTPStatus.OK
    assert 'access_token' in login_response.json()


@pytest.mark.asyncio
async def test_change_password_me_mismatch(api_client, user_token):
    """Test changing password with mismatched passwords"""
    response = api_client.patch(
        '/users/me/change-password',
        json={
            'password': 'password1',
            'password_confirmation': 'password2',
        },
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Passwords dont match.'


@pytest.mark.asyncio
async def test_delete_user_me(api_client, user, user_token):
    """Test user can delete (deactivate) their own account"""
    response = api_client.delete(
        '/users/me',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['message'] == 'User deleted.'

    # Verify login no longer works with deactivated account
    login_response = api_client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
        headers={'X-Tenant-Domain': user.tenant.domain},
    )
    # Login should fail - accept 400 or 401
    assert login_response.status_code in {
        HTTPStatus.BAD_REQUEST,
        HTTPStatus.UNAUTHORIZED,
    }
