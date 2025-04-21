from datetime import date
from http import HTTPStatus
from uuid import UUID

import pytest_asyncio

from src.models import Task


@pytest_asyncio.fixture
async def db_task(session, db_project, superuser, tenant) -> Task:
    task = Task(
        title='Test Task',
        description='This is a test task',
        status='to_do',
        priority='medium',
        due_date=date(2024, 12, 31),
        project_id=db_project.id,
        created_by=superuser.id,
        tenant_id=tenant.id,
        is_active=True,
    )
    # Set relationships after creation
    task.project = db_project
    task.tenant = tenant

    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


def test_create_task(api_client, db_project, superuser_token) -> None:
    response = api_client.post(
        url='/tasks',
        json={
            'title': 'New Task',
            'description': 'This is a new task',
            'status': 'to_do',
            'priority': 'high',
            'due_date': '2024-12-31',
            'project_id': str(db_project.id),
        },
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['title'] == 'New Task'
    assert data['description'] == 'This is a new task'
    assert data['status'] == 'to_do'
    assert data['priority'] == 'high'
    assert data['due_date'] == '2024-12-31'
    assert UUID(data['project_id']) is not None
    assert data['is_active'] is True
    assert UUID(data['created_by']) is not None
    if 'updated_by' in data:
        assert data['updated_by'] is None


def test_create_task_project_not_found(api_client, superuser_token) -> None:
    response = api_client.post(
        url='/tasks',
        json={
            'title': 'New Task',
            'description': 'This is a new task',
            'status': 'to_do',
            'priority': 'high',
            'due_date': '2024-12-31',
            'project_id': '123e4567-e89b-12d3-a456-426614174000',
        },
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': "Project doesn't exist"}


def test_read_task_by_id(
    session, db_task, api_client, superuser_token
) -> None:
    response = api_client.get(
        url=f'/tasks/{db_task.id}',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['id'] == str(db_task.id)
    assert data['title'] == db_task.title
    assert data['description'] == db_task.description
    assert data['status'] == db_task.status
    assert data['priority'] == db_task.priority
    assert data['due_date'] == db_task.due_date.isoformat()
    assert data['project_id'] == str(db_task.project_id)
    assert data['is_active'] == db_task.is_active
    assert UUID(data['created_by']) == db_task.created_by
    if 'updated_by' in data:
        assert data['updated_by'] is None


def test_read_task_by_id_not_found(api_client, superuser_token) -> None:
    response = api_client.get(
        url='/tasks/123e4567-e89b-12d3-a456-426614174000',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': "Task doesn't exist"}


def test_read_all_tasks(session, db_task, api_client, superuser_token) -> None:
    response = api_client.get(
        url='/tasks',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'tasks' in data
    assert len(data['tasks']) == 1
    assert data['tasks'][0]['id'] == str(db_task.id)


def test_read_all_tasks_filter_by_project(
    session, db_task, db_project, api_client, superuser_token
) -> None:
    response = api_client.get(
        url=f'/tasks?project_id={db_project.id}',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'tasks' in data
    assert len(data['tasks']) == 1
    assert data['tasks'][0]['id'] == str(db_task.id)


def test_read_all_tasks_filter_by_project_no_results(
    session, db_task, api_client, superuser_token
) -> None:
    response = api_client.get(
        url='/tasks?project_id=123e4567-e89b-12d3-a456-426614174000',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'tasks' in data
    assert len(data['tasks']) == 0


def test_update_task(session, db_task, api_client, superuser_token) -> None:
    response = api_client.patch(
        url=f'/tasks/{db_task.id}',
        json={'title': 'Updated Task Title', 'status': 'in_progress'},
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['title'] == 'Updated Task Title'
    assert data['status'] == 'in_progress'
    assert data['description'] == db_task.description
    assert data['priority'] == db_task.priority
    assert data['due_date'] == db_task.due_date.isoformat()
    assert UUID(data['updated_by']) is not None


def test_update_task_not_found(api_client, superuser_token) -> None:
    response = api_client.patch(
        url='/tasks/123e4567-e89b-12d3-a456-426614174000',
        json={'title': 'Updated Task Title'},
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': "Task doesn't exist"}


def test_update_task_project_not_found(
    api_client, db_task, superuser_token
) -> None:
    response = api_client.patch(
        url=f'/tasks/{db_task.id}',
        json={'project_id': '123e4567-e89b-12d3-a456-426614174000'},
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': "Project doesn't exist"}


def test_delete_task(api_client, db_task, superuser_token) -> None:
    response = api_client.delete(
        url=f'/tasks/{db_task.id}',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task deleted'}


def test_delete_task_not_found(api_client, superuser_token) -> None:
    response = api_client.delete(
        url='/tasks/123e4567-e89b-12d3-a456-426614174000',
        headers={'Authorization': f'Bearer {superuser_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': "Task doesn't exist"}
