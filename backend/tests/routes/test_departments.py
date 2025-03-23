from http import HTTPStatus

import pytest_asyncio

from src.models import Department
from src.schemas.departments import DepartmentPublic


@pytest_asyncio.fixture
async def department(session):
    department = Department(name='test_department')

    session.add(department)
    await session.commit()
    await session.refresh(department)

    return department


def test_create_department(api_client):
    response = api_client.post(
        '/departments/', json={'name': 'test_department'}
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'name': 'test_department'}


def test_create_department_already_exists(api_client, department):
    response = api_client.post(
        '/departments/', json={'name': 'test_department'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Department already exists'}


def test_read_test_department(api_client, department):
    department_schema = DepartmentPublic.model_validate(
        department
    ).model_dump()

    response = api_client.get('/departments/test_department')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == department_schema


def test_read_departments(api_client):
    response = api_client.get('/departments')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'departments': []}


def test_read_departments_with_department(api_client, department):
    department_schema = DepartmentPublic.model_validate(
        department
    ).model_dump()
    response = api_client.get('/departments')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'departments': [department_schema]}


def test_delete_department(api_client, department):
    response = api_client.delete('/departments/test_department')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Department deleted'}


def test_delete_department_not_exists(api_client):
    response = api_client.delete('/departments/test_department')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Department not found'}


def test_update_department(api_client, department):
    response = api_client.put(
        'departments/1', json={'name': 'test_department_updated'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': 1, 'name': 'test_department_updated'}


def test_update_department_not_found(api_client):
    response = api_client.put(
        '/departments/1', json={'name': 'test_department'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Department not found'}


def test_update_integrity_error(api_client, department):
    # Criando um registro para "test_department_novo"
    api_client.post('/departments', json={'name': 'test_department_novo'})

    # Alterando o department.name das fixture para test_department_novo
    response_update = api_client.put(
        f'/departments/{department.id}', json={'name': 'test_department_novo'}
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'Department already exists'}
