from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import engine
from src.core.settings import settings
from src.models import User


async def get_session():  # pragma: no cover
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


T_Session = Annotated[AsyncSession, Depends(get_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_current_user(
    session: T_Session,
    token: str = Depends(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        subject_email = payload.get('sub')

        if not subject_email:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception

    user_db = await session.scalar(
        select(User).where(
            (User.email == subject_email) & (User.is_active == True)  # noqa: E712
        )
    )

    if not user_db:
        raise credentials_exception

    return user_db


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user


def validate_user_access(current_user: CurrentUser, user_id: UUID) -> bool:
    """
    Validate if current user has access to the requested user information:
    - Superusers can access any user
    - Regular users can only access their own information
    """
    if current_user.is_superuser:
        return True

    if str(current_user.id) == str(user_id):
        return True

    raise HTTPException(
        status_code=HTTPStatus.FORBIDDEN,
        detail='Access denied: You can only access your own information',
    )
