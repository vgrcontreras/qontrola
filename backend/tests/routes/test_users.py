from http import HTTPStatus

from src.schemas.users import UserPublic


def test_create_user(api_client, superuser_token):
    response = api_client.post(
        '/users/',
        json={
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@test.com',
            'password': 'test_password',
            'salary': 1000,
            'is_superuser': False,
        },
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 2,
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test@test.com',
        'is_superuser': False,
        'is_active': True,
    }


def test_create_user_already_exists(api_client, superuser_token):
    response = api_client.post(
        '/users/',
        json={
            'first_name': 'test',
            'last_name': 'test',
            'email': 'admin@admin.com',
            'password': 'test_password',
            'is_superuser': False,
            'salary': 1000,
        },
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'User already exists'}


def test_delete_user(api_client, user, superuser_token):
    response = api_client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(api_client, superuser_token):
    response = api_client.delete(
        '/users/2', headers={'Authorization': f'Bearer {superuser_token}'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'User Not Found'}


def test_read_users(api_client):
    response = api_client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(api_client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = api_client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user_not_found(api_client, superuser_token):
    response = api_client.patch(
        '/users/2',
        json={'salary': 300},
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'User Not Found'}


def test_update_user_integrity_error(api_client, user, superuser_token):
    # criando novo usuário
    api_client.post(
        '/users/',
        json={
            'first_name': 'name_test',
            'last_name': 'surname_test',
            'email': 'test@email.com',
            'password': 'test_password',
            'salary': 100,
        },
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    # alterando email do novo usuário para e-mail já existente

    response_update = api_client.patch(
        f'/users/{user.id}',
        json={'email': 'test@email.com'},
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'User email already exists'}


def test_update_user(api_client, user, superuser_token):
    response = api_client.patch(
        f'/users/{user.id}',
        json={'salary': 300},
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test@test.com',
        'salary': 300.0,
        'is_superuser': False,
        'is_active': True,
    }


def test_update_user_not_superuser(api_client, user, user_token):
    response = api_client.patch(
        f'/users/{user.id}',
        json={'salary': 300},
        headers={'Authorization': f'Bearer {user_token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': "The user doesn't have enough previleges"
    }


def test_update_user_password(api_client, user, superuser_token):
    response = api_client.patch(
        f'/users/{user.id}',
        json={'password': 'new_password'},
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test@test.com',
        'salary': 1000.0,
        'is_superuser': False,
        'is_active': True,
    }
