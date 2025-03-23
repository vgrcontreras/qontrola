from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import (
    T_Session,
    get_current_active_superuser,
)
from src.models import User
from src.schemas.base import Message
from src.schemas.users import (
    UserList,
    UserPublic,
    UserPublicSalary,
    UserSchema,
    UserUpdate,
)
from src.security import get_password_hash

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
    dependencies=[Depends(get_current_active_superuser)],
)
async def create_user(user: UserSchema, session: T_Session):
    db_user = await session.scalar(
        select(User).where(User.email == user.email)
    )

    if db_user is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='User already exists'
        )

    user_attrs = user.model_dump()

    user_attrs['password'] = get_password_hash(user.password)

    new_user = User(**user_attrs)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
async def read_users(session: T_Session):
    db_users = await session.scalars(select(User))

    return {'users': db_users}


@router.delete(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
    dependencies=[Depends(get_current_active_superuser)],
)
async def delete_user(
    user_id: int,
    session: T_Session,
):
    db_user = await session.scalar(select(User).where(User.id == user_id))

    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='User Not Found'
        )

    db_user.is_active = False

    session.add(db_user)
    await session.commit()

    return {'message': 'User deleted'}


@router.patch(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublicSalary,
    dependencies=[Depends(get_current_active_superuser)],
)
async def update_user(
    user_id: int,
    user: UserUpdate,
    session: T_Session,
):
    db_user = await session.scalar(select(User).where(User.id == user_id))

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
        await session.commit()
        await session.refresh(db_user)

        return db_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='User email already exists'
        )
