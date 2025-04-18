from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import engine
from src.core.settings import settings
from src.models import Tenant, User


async def get_session():  # pragma: no cover
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


T_Session = Annotated[AsyncSession, Depends(get_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_tenant_from_domain(
    session: T_Session, x_tenant_domain: str | None = Header(None)
) -> Tenant:
    """Get tenant from domain header"""
    if not x_tenant_domain:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='X-Tenant-Domain header is required',
        )

    tenant = await session.scalar(
        select(Tenant).where(
            (Tenant.domain == x_tenant_domain) & (Tenant.is_active == True)  # noqa: E712
        )
    )

    if not tenant:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Tenant not found or inactive',
        )

    return tenant


CurrentTenant = Annotated[Tenant, Depends(get_tenant_from_domain)]


async def get_current_user(
    session: T_Session,
    tenant: CurrentTenant,
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
        token_tenant_id = payload.get('tenant_id')

        if not subject_email or not token_tenant_id:
            raise credentials_exception

        # Verify that the token's tenant matches the request tenant
        if str(tenant.id) != token_tenant_id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='Token tenant does not match request tenant',
            )

    except DecodeError:
        raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception

    user_db = await session.scalar(
        select(User).where(
            (User.email == subject_email)
            & (User.tenant_id == tenant.id)
            & (User.is_active == True)  # noqa: E712
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


def validate_user_tenant_access(
    current_user: CurrentUser, user_id: UUID
) -> bool:
    """
    Validate if current user has access to the requested user information:
    - Superusers can access any user within their tenant
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
