from datetime import date
from http import HTTPStatus
from uuid import UUID

import pytest_asyncio

from src.models import Project


@pytest_asyncio.fixture
async def db_project(session, superuser, tenant) -> Project:
    project = Project(
        name='test_project',
        status_state='active',
        project_value=1000.0,
        target_date=date(2024, 12, 31),
        created_by=superuser.id,
        is_active=True,
        tenant_id=tenant.id,
        tenant=tenant,
    )
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


def test_create_project(api_client, superuser_token) -> None:
    response = api_client.post(
        url='/projects',
        json={
            'name': 'project1',
            'status_state': 'active',
            'project_value': 1000.0,
            'target_date': '2024-12-31',
        },
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    PROJECT_VALUE = 1000.0

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['name'] == 'project1'
    assert data['status_state'] == 'active'
    assert data['project_value'] == PROJECT_VALUE
    assert data['target_date'] == '2024-12-31'
    assert data['is_active'] is True
    assert UUID(data['created_by']) is not None
    # updated_by might not be included in the response
    if 'updated_by' in data:
        assert data['updated_by'] is None


def test_create_project_already_exists(
    api_client, db_project, superuser_token
) -> None:
    response = api_client.post(
        url='/projects',
        json={
            'name': 'test_project',
            'status_state': 'active',
            'project_value': 1000.0,
            'target_date': '2024-12-31',
        },
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Project already exists'}


def test_delete_project(api_client, db_project, superuser_token) -> None:
    response = api_client.delete(
        url=f'/projects/{db_project.id}',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Project deleted'}


def test_delete_project_not_found(api_client, superuser_token) -> None:
    response = api_client.delete(
        url='/projects/123e4567-e89b-12d3-a456-426614174000',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': "Project doesn't exist"}


def test_update_project_not_found(api_client, superuser_token) -> None:
    response = api_client.patch(
        url='/projects/123e4567-e89b-12d3-a456-426614174000',
        json={'name': 'test_update_name'},
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': "Project doesn't exist"}


def test_update_project(api_client, db_project, superuser_token) -> None:
    response = api_client.patch(
        url=f'/projects/{db_project.id}',
        json={'name': 'test_updated_name'},
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    PROJECT_VALUE = 1000.0

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['name'] == 'test_updated_name'
    assert data['status_state'] == 'active'
    assert data['project_value'] == PROJECT_VALUE
    assert data['target_date'] == '2024-12-31'
    assert data['is_active'] is True
    assert UUID(data['created_by']) is not None
    assert UUID(data['updated_by']) is not None


def test_update_project_integrity_error(
    api_client, db_project, superuser_token
) -> None:
    # creating a new project
    api_client.post(
        url='/projects',
        json={
            'name': 'project2',
            'status_state': 'active',
            'project_value': 1000.0,
            'target_date': '2024-12-31',
        },
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    response = api_client.patch(
        url=f'/projects/{db_project.id}',
        json={'name': 'project2'},
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Project already exists'}


def test_get_all_projects(session, api_client, superuser_token) -> None:
    response = api_client.get(
        url='/projects',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'projects': []}


def test_get_project_by_id(
    session, db_project, api_client, superuser_token
) -> None:
    response = api_client.get(
        url=f'/projects/{db_project.id}',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['id'] == str(db_project.id)
    assert data['name'] == db_project.name
    assert data['status_state'] == db_project.status_state
    assert data['project_value'] == db_project.project_value
    assert data['target_date'] == db_project.target_date.isoformat()
    assert data['is_active'] == db_project.is_active
    assert UUID(data['created_by']) == db_project.created_by
    # updated_by might not be included in the response
    if 'updated_by' in data:
        assert data['updated_by'] is None


def test_get_project_by_id_not_found(
    session, api_client, superuser_token
) -> None:
    response = api_client.get(
        url='/projects/123e4567-e89b-12d3-a456-426614174000',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': "Project doesn't exist"}
