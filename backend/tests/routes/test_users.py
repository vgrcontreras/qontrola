from http import HTTPStatus

import pytest

from src.models import User
from src.schemas.users import UserPublic


@pytest.fixture
def user(session):
    new_user = User(
        first_name='test',
        last_name='test',
        email='test@test.com',
        password='test_password',
        salary=1000,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@test.com',
            'password': 'test_password',
            'salary': 1000,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test@test.com',
        'is_active': True,
    }


def test_create_user_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@test.com',
            'password': 'test_password',
            'salary': 1000,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'User already exists'}


def test_delete_user(client, user):
    response = client.delete(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'User Not Found'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user_not_found(client):
    response = client.patch('/users/1', json={'salary': 300})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'User Not Found'}


def test_update_user_integrity_error(client, user):
    # criando novo usuário
    client.post(
        '/users/',
        json={
            'first_name': 'name_test',
            'last_name': 'surname_test',
            'email': 'test@email.com',
            'password': 'test_password',
            'salary': 100,
        },
    )

    # alterando email do novo usuário para e-mail já existente

    response_update = client.patch('/users/2', json={'email': 'test@test.com'})

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'User email already exists'}


def test_update_user(client, user):
    response = client.patch('/users/1', json={'salary': 300})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test@test.com',
        'salary': 300.0,
        'is_active': True,
    }
