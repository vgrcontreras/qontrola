# from .models import
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import get_session
from backend.models import Department
from backend.schemas import DepartmentPublic, DepartmentSchema, Message

app = FastAPI()

T_Session = Annotated[Session, Depends(get_session)]


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post(
    '/departments/',
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
