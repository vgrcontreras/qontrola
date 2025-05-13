from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import (
    CurrentTenant,
    CurrentUser,
    T_Session,
    get_current_active_superuser,
)
from src.models import Project
from src.schemas.base import Message
from src.schemas.projects import (
    ProjectRequestCreate,
    ProjectRequestGet,
    ProjectRequestGetList,
    ProjectResponse,
    ProjectResquestUpdate,
)
from src.utils.category_utils import get_or_create_category

router = APIRouter()


@router.post(
    path='/',
    status_code=HTTPStatus.CREATED,
    response_model=ProjectResponse,
)
async def create_project(
    session: T_Session,
    project: ProjectRequestCreate,
    current_user: CurrentUser,
    tenant: CurrentTenant,
) -> Project:
    """Create a new project within the current tenant."""
    # Check if project exists in this tenant
    project_db = await session.scalar(
        select(Project).where(
            Project.name == project.name, Project.tenant_id == tenant.id
        )
    )

    if project_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Project already exists'
        )

    project_data = project.model_dump()

    # Handle category_name if provided
    category_name = project_data.pop('category_name', None)
    if category_name:
        category = await get_or_create_category(
            db=session, category_name=category_name, tenant_id=tenant.id
        )
        if category:
            project_data['category_id'] = category.id

    # Set the fields from the request
    project_data['created_by'] = current_user.id
    project_data['tenant_id'] = tenant.id

    # Create the project with the provided data
    project_db = Project(**project_data)

    session.add(project_db)
    await session.commit()
    await session.refresh(project_db)

    return project_db


@router.get(
    path='/{project_id}',
    status_code=HTTPStatus.OK,
    response_model=ProjectRequestGet,
)
async def read_project_by_id(
    session: T_Session,
    project_id: UUID,
    tenant: CurrentTenant,
    current_user: CurrentUser,
) -> Project:
    """
    Get a specific project from the current tenant.
    """
    query = select(Project).where(
        Project.id == project_id, Project.tenant_id == tenant.id
    )

    project_db = await session.scalar(query)

    if not project_db:
        raise HTTPException(
            detail="Project doesn't exist", status_code=HTTPStatus.NOT_FOUND
        )

    return project_db


@router.get(
    path='/',
    status_code=HTTPStatus.OK,
    response_model=ProjectRequestGetList,
)
async def read_all_projects(
    session: T_Session,
    tenant: CurrentTenant,
    current_user: CurrentUser,
) -> list[Project]:
    """
    Get all projects within the current tenant.
    """
    query = select(Project).where(Project.tenant_id == tenant.id)

    projects_db = await session.scalars(query)

    return {'projects': projects_db.all()}


@router.delete(
    path='/{project_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
    dependencies=[Depends(get_current_active_superuser)],
)
async def delete_project(
    session: T_Session,
    project_id: UUID,
    current_user: CurrentUser,
    tenant: CurrentTenant,
) -> dict:
    """
    Delete (deactivate) a project from the current tenant.
    """
    project_db = await session.scalar(
        select(Project).where(
            Project.id == project_id, Project.tenant_id == tenant.id
        )
    )

    if not project_db:
        raise HTTPException(
            detail="Project doesn't exist", status_code=HTTPStatus.NOT_FOUND
        )

    project_db.is_active = False
    project_db.updated_by = current_user.id

    session.add(project_db)
    await session.commit()

    return {'message': 'Project deleted'}


@router.patch(
    path='/{project_id}',
    status_code=HTTPStatus.OK,
    response_model=ProjectRequestGet,
)
async def update_project(
    session: T_Session,
    project_id: UUID,
    project: ProjectResquestUpdate,
    current_user: CurrentUser,
    tenant: CurrentTenant,
) -> Project:
    """Update a project within the current tenant."""
    project_db = await session.scalar(
        select(Project).where(
            Project.id == project_id, Project.tenant_id == tenant.id
        )
    )

    try:
        if not project_db:
            raise HTTPException(
                detail="Project doesn't exist",
                status_code=HTTPStatus.NOT_FOUND,
            )

        project_data = project.model_dump(exclude_unset=True)

        # Handle category_name if provided
        category_name = project_data.pop('category_name', None)
        if category_name:
            category = await get_or_create_category(
                db=session, category_name=category_name, tenant_id=tenant.id
            )
            if category:
                project_data['category_id'] = category.id

        project_data['updated_by'] = current_user.id

        for key, value in project_data.items():
            setattr(project_db, key, value)

        session.add(project_db)
        await session.commit()
        await session.refresh(project_db)

        return project_db

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Project already exists'
        )
