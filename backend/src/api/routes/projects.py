from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import T_Session, get_current_user
from src.models import Project, User
from src.schemas.base import Message
from src.schemas.projects import (
    ProjectRequestCreate,
    ProjectRequestGet,
    ProjectRequestGetList,
    ProjectResponse,
    ProjectResquestUpdate,
)

router = APIRouter(prefix='/projects', tags=['projects'])


@router.post(
    path='/',
    status_code=HTTPStatus.CREATED,
    response_model=ProjectResponse,
)
async def create_project(
    session: T_Session,
    project: ProjectRequestCreate,
    current_user: User = Depends(get_current_user),
) -> Project:
    project_db = await session.scalar(
        select(Project).where(Project.name == project.name)
    )

    if project_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Project already exists'
        )

    project_data = project.model_dump()

    project_data['created_by'] = current_user.id

    project_db = Project(**project_data)

    session.add(project_db)
    await session.commit()
    await session.refresh(project_db)

    return project_db


@router.get(
    path='/{project_id}',
    status_code=HTTPStatus.OK,
    response_model=ProjectRequestGet,
    dependencies=[Depends(get_current_user)],
)
async def read_project_by_id(session: T_Session, project_id: int) -> Project:
    project_db = await session.scalar(
        select(Project).where(Project.id == project_id)
    )

    if not project_db:
        raise HTTPException(
            detail="Project doesn't exists", status_code=HTTPStatus.BAD_REQUEST
        )

    return project_db


@router.get(
    path='/',
    status_code=HTTPStatus.OK,
    response_model=ProjectRequestGetList,
    dependencies=[Depends(get_current_user)],
)
async def read_all_projects(session: T_Session) -> list[Project]:
    projects_db = await session.scalars(select(Project))

    return {'projects': projects_db}


@router.delete(
    path='/{project_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
    dependencies=[Depends(get_current_user)],
)
async def delete_project(session: T_Session, project_id: int) -> dict:
    project_db = await session.scalar(
        select(Project).where(Project.id == project_id)
    )

    project_db.is_active = False

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
    project_id: int,
    project: ProjectResquestUpdate,
    current_user: User = Depends(get_current_user),
) -> Project:
    project_db = await session.scalar(
        select(Project).where(Project.id == project_id)
    )

    try:
        if not project_db:
            raise HTTPException(
                detail="Project doesn't exists",
                status_code=HTTPStatus.BAD_REQUEST,
            )

        project_data = project.model_dump(exclude_unset=True)

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
