from http import HTTPStatus

import pytest

from src.models import Department
from src.schemas import DepartmentPublic


@pytest.fixture
def department(session):
    department = Department(name='test_department')

    session.add(department)
    session.commit()
    session.refresh(department)

    return department


def test_create_department(client):
    response = client.post('/departments/', json={'name': 'test_department'})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'name': 'test_department'}


def test_create_department_already_exists(client, department):
    response = client.post('/departments/', json={'name': 'test_department'})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Department already exists'}


def test_read_test_department(client, department):
    department_schema = DepartmentPublic.model_validate(
        department
    ).model_dump()

    response = client.get('/departments/test_department')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == department_schema


def test_read_departments(client):
    response = client.get('/departments')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'departments': []}


def test_read_departments_with_department(client, department):
    department_schema = DepartmentPublic.model_validate(
        department
    ).model_dump()
    response = client.get('/departments')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'departments': [department_schema]}


def test_delete_department(client, department):
    response = client.delete('/departments/test_department')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Department deleted'}


def test_delete_department_not_exists(client):
    response = client.delete('/departments/test_department')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Department not found'}


def test_update_department(client, department):
    response = client.put(
        'departments/1', json={'name': 'test_department_updated'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': 1, 'name': 'test_department_updated'}


def test_update_department_not_found(client):
    response = client.put('/departments/1', json={'name': 'test_department'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Department not found'}


def test_update_integrity_error(client, department):
    # Criando um registro para "test_department_novo"
    client.post('/departments', json={'name': 'test_department_novo'})

    # Alterando o department.name das fixture para test_department_novo
    response_update = client.put(
        f'/departments/{department.id}', json={'name': 'test_department_novo'}
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'Department already exists'}
