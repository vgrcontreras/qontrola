from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import (
    CurrentTenant,
    T_Session,
    get_current_active_superuser,
)
from src.models import User
from src.schemas.base import Message
from src.schemas.users import UserList, UserPublic, UserSchema, UserUpdate
from src.security import get_password_hash

router = APIRouter(dependencies=[Depends(get_current_active_superuser)])


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
)
async def create_user(
    user: UserSchema, session: T_Session, tenant: CurrentTenant
):
    db_user = await session.scalar(
        select(User).where(
            User.email == user.email, User.tenant_id == tenant.id
        )
    )

    if db_user is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='User already exists'
        )

    user_attrs = user.model_dump()
    user_attrs['password'] = get_password_hash(user.password)
    user_attrs['tenant_id'] = tenant.id
    user_attrs['tenant'] = tenant

    new_user = User(**user_attrs)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
async def read_users(
    session: T_Session,
    tenant: CurrentTenant,
):
    """
    Get all users within the current tenant.
    """
    query = select(User).where(User.tenant_id == tenant.id)

    db_users = await session.scalars(query)

    return {'users': db_users.all()}


@router.get('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
async def read_user(
    user_id: UUID,
    session: T_Session,
    tenant: CurrentTenant,
):
    """
    Get a specific user from the current tenant.
    """
    query = select(User).where(User.id == user_id, User.tenant_id == tenant.id)

    db_user = await session.scalar(query)

    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found'
        )

    return db_user


@router.delete(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
async def delete_user(
    user_id: UUID,
    session: T_Session,
    tenant: CurrentTenant,
):
    db_user = await session.scalar(
        select(User).where(User.id == user_id, User.tenant_id == tenant.id)
    )

    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found'
        )

    db_user.is_active = False

    session.add(db_user)
    await session.commit()

    return {'message': 'User deleted'}


@router.patch(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
)
async def update_user(
    user_id: UUID,
    user: UserUpdate,
    session: T_Session,
    tenant: CurrentTenant,
):
    db_user = await session.scalar(
        select(User).where(User.id == user_id, User.tenant_id == tenant.id)
    )

    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found'
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
