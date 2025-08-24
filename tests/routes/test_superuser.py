from http import HTTPStatus
from uuid import UUID

from src.schemas.users import UserPublic


def test_create_user(api_client, superuser_token):
    response = api_client.post(
        '/superuser/',
        json={
            'full_name': 'test',
            'email': 'test@test.com',
            'password': 'test_password',
            'is_superuser': False,
        },
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['full_name'] == 'test'
    assert data['email'] == 'test@test.com'
    assert data['is_superuser'] is False
    assert data['is_active'] is True
    assert UUID(data['id']) is not None


def test_create_user_already_exists(api_client, superuser_token):
    response = api_client.post(
        '/superuser/',
        json={
            'full_name': 'test',
            'email': 'admin@admin.com',
            'password': 'test_password',
            'is_superuser': False,
        },
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'User already exists'}


def test_delete_user(api_client, user, superuser_token):
    response = api_client.delete(
        f'/superuser/{user.id}',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(api_client, superuser_token):
    response = api_client.delete(
        '/superuser/123e4567-e89b-12d3-a456-426614174000',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_read_users_with_user(api_client, user, user_token):
    user_schema = UserPublic.model_validate(user).model_dump()
    # Convert UUID to string for comparison with JSON response
    user_schema['id'] = str(user_schema['id'])

    response = api_client.get(
        f'/superuser/{user.id}',
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': "The user doesn't have enough privileges"
    }


def test_update_user_not_found(api_client, superuser_token):
    response = api_client.patch(
        '/superuser/123e4567-e89b-12d3-a456-426614174000',
        json={'full_name': 'new_name'},
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_update_user_integrity_error(api_client, user, superuser_token):
    # creating new user
    api_client.post(
        '/superuser/',
        json={
            'full_name': 'name_test',
            'email': 'test@email.com',
            'password': 'test_password',
        },
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    # changing email of the new user to an already existing email
    response_update = api_client.patch(
        f'/superuser/{user.id}',
        json={'email': 'test@email.com'},
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'User email already exists'}


def test_update_user(api_client, user, superuser_token):
    response = api_client.patch(
        f'/superuser/{user.id}',
        json={'full_name': 'new_name'},
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert UUID(data['id']) == user.id
    assert data['full_name'] == 'new_name'
    assert data['email'] == 'test@test.com'
    assert data['is_superuser'] is False
    assert data['is_active'] is True


def test_update_user_not_superuser(api_client, user, user_token):
    response = api_client.patch(
        f'/superuser/{user.id}',
        json={'full_name': 'new_name'},
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': "The user doesn't have enough privileges"
    }


def test_update_user_password(api_client, user, superuser_token):
    response = api_client.patch(
        f'/superuser/{user.id}',
        json={'password': 'new_password'},
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert UUID(data['id']) == user.id
    assert data['full_name'] == 'test'
    assert data['email'] == 'test@test.com'
    assert data['is_superuser'] is False
    assert data['is_active'] is True
