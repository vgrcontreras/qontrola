from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import Department
from src.schemas.departments import (
    DepartmentPublic,
    DepartmentPublicList,
    DepartmentSchema,
    Message,
)

router = APIRouter(prefix='/departments', tags=['departments'])

T_Session = Annotated[Session, Depends(get_session)]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=DepartmentPublic,
)
def create_department(department: DepartmentSchema, session: T_Session):
    db_department = session.scalar(
        select(Department).where(Department.name == department.name)
    )

    if db_department is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Department already exists',
        )

    db_department = Department(name=department.name)

    session.add(db_department)
    session.commit()
    session.refresh(db_department)

    return db_department


@router.get(
    '/{department_name}',
    status_code=HTTPStatus.OK,
    response_model=DepartmentPublic,
)
def read_department(department_name: str, session: T_Session):
    db_department = session.scalar(
        select(Department).where(Department.name == department_name)
    )

    return db_department


@router.get(
    '/', status_code=HTTPStatus.OK, response_model=DepartmentPublicList
)
def read_all_departments(session: T_Session):
    db_departments = session.scalars(select(Department)).all()

    return {'departments': db_departments}


@router.delete(
    '/{department_name}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_department(department_name: str, session: T_Session):
    db_department = session.scalar(
        select(Department).where(Department.name == department_name)
    )

    if db_department is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Department not found'
        )

    session.delete(db_department)
    session.commit()

    return {'message': 'Department deleted'}


@router.put(
    '/{department_id}',
    status_code=HTTPStatus.OK,
    response_model=DepartmentPublic,
)
def update_department(
    department_id: int, department: DepartmentSchema, session: T_Session
):
    db_department = session.scalar(
        select(Department).where(Department.id == department_id)
    )

    if db_department is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Department not found'
        )

    try:
        db_department.name = department.name

        session.commit()
        session.refresh(db_department)

        return db_department

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Department already exists'
        )
