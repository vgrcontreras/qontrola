from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import User
from src.schemas.base import Message
from src.schemas.users import (
    UserList,
    UserPublic,
    UserPublicSalary,
    UserSchema,
    UserUpdate,
)
from src.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])

T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):
    db_user = session.scalar(select(User).where(User.email == user.email))

    if db_user is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='User already exists'
        )

    user_attrs = user.model_dump()

    user_attrs['password'] = get_password_hash(user.password)

    new_user = User(**user_attrs)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(session: T_Session):
    db_users = session.scalars(select(User))

    return {'users': db_users}


@router.delete('/{user_id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_user(
    user_id: int, session: T_Session, current_user=Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not Enough Permission'
        )

    db_user = session.scalar(select(User).where(User.id == user_id))

    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='User Not Found'
        )

    db_user.is_active = False

    session.add(db_user)
    session.commit()

    return {'message': 'User deleted'}


@router.patch(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublicSalary
)
def update_user(
    user_id: int,
    user: UserUpdate,
    session: T_Session,
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not Enough Permission'
        )

    db_user = session.scalar(select(User).where(User.id == user_id))

    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='User Not Found'
        )

    try:
        user_data = user.model_dump(exclude_unset=True)

        if 'password' in user_data:
            user_data['password'] = get_password_hash(user_data['password'])

        for key, value in user_data.items():
            setattr(db_user, key, value)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='User email already exists'
        )
