from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from src.api.dependencies import CurrentUser, T_Session
from src.models import Project, Task
from src.schemas.base import Message
from src.schemas.tasks import (
    TaskRequestCreate,
    TaskRequestGet,
    TaskRequestGetList,
    TaskRequestUpdate,
    TaskResponse,
)
from src.utils.category_utils import get_or_create_category

router = APIRouter()


@router.post(
    path='/',
    status_code=HTTPStatus.CREATED,
    response_model=TaskResponse,
)
async def create_task(
    session: T_Session,
    task: TaskRequestCreate,
    current_user: CurrentUser,
) -> Task:
    """Create a new task."""
    # Check if project exists
    project_db = await session.scalar(
        select(Project).where(Project.id == task.project_id)
    )

    if not project_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Project doesn't exist"
        )

    task_data = task.model_dump()

    # Handle category_name if provided
    category_name = task_data.pop('category_name', None)
    if category_name:
        category = await get_or_create_category(
            db=session, category_name=category_name
        )
        if category:
            task_data['category_id'] = category.id

    task_data['created_by'] = current_user.id

    # Create task instance
    task_db = Task(**task_data)
    # Set relationships after creation
    task_db.project = project_db

    session.add(task_db)
    await session.commit()
    await session.refresh(task_db)

    return task_db


@router.get(
    path='/{task_id}',
    status_code=HTTPStatus.OK,
    response_model=TaskRequestGet,
)
async def read_task_by_id(
    session: T_Session,
    task_id: UUID,
    current_user: CurrentUser,
) -> Task:
    """
    Get a specific task.
    """
    query = select(Task).where(Task.id == task_id)

    task_db = await session.scalar(query)

    if not task_db:
        raise HTTPException(
            detail="Task doesn't exist", status_code=HTTPStatus.NOT_FOUND
        )

    return task_db


@router.get(
    path='/',
    status_code=HTTPStatus.OK,
    response_model=TaskRequestGetList,
)
async def read_all_tasks(
    session: T_Session,
    current_user: CurrentUser,
    project_id: UUID | None = None,
) -> dict:
    """
    Get all tasks.
    Optionally filter by project_id.
    """
    query = select(Task)

    if project_id:
        query = query.where(Task.project_id == project_id)

    tasks_db = await session.scalars(query)

    return {'tasks': tasks_db.all()}


@router.delete(
    path='/{task_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
async def delete_task(
    session: T_Session,
    task_id: UUID,
    current_user: CurrentUser,
) -> dict:
    """
    Delete (deactivate) a task.
    """
    task_db = await session.scalar(select(Task).where(Task.id == task_id))

    if not task_db:
        raise HTTPException(
            detail="Task doesn't exist", status_code=HTTPStatus.NOT_FOUND
        )

    task_db.is_active = False
    task_db.updated_by = current_user.id

    session.add(task_db)
    await session.commit()

    return {'message': 'Task deleted'}


@router.patch(
    path='/{task_id}',
    status_code=HTTPStatus.OK,
    response_model=TaskRequestGet,
)
async def update_task(
    session: T_Session,
    task_id: UUID,
    task: TaskRequestUpdate,
    current_user: CurrentUser,
) -> Task:
    """Update a task."""
    task_db = await session.scalar(select(Task).where(Task.id == task_id))

    if not task_db:
        raise HTTPException(
            detail="Task doesn't exist",
            status_code=HTTPStatus.NOT_FOUND,
        )

    task_data = task.model_dump(exclude_unset=True)

    # Handle category_name if provided
    category_name = task_data.pop('category_name', None)
    if category_name:
        category = await get_or_create_category(
            db=session, category_name=category_name
        )
        if category:
            task_data['category_id'] = category.id

    # If project_id is provided, verify the project exists
    if task_data.get('project_id'):
        project_db = await session.scalar(
            select(Project).where(
                Project.id == task_data['project_id'],
            )
        )

        if not project_db:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Project doesn't exist",
            )
        # Set project relationship separately
        task_db.project = project_db
        # Remove project key from data to avoid errors
        task_data.pop('project_id')

    task_data['updated_by'] = current_user.id

    for key, value in task_data.items():
        setattr(task_db, key, value)

    session.add(task_db)
    await session.commit()
    await session.refresh(task_db)

    return task_db
