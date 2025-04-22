from http import HTTPStatus

from fastapi import APIRouter, Depends, Header
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from src.api.dependencies import CurrentTenant, CurrentUser, T_Session
from src.models import Tenant, User
from src.schemas.token import EmailRequest, TenantDomainResponse, Token
from src.security import create_access_token, verify_password

router = APIRouter()


@router.post('/', status_code=HTTPStatus.OK, response_model=Token)
async def login_for_access_token(
    session: T_Session,
    form_data: OAuth2PasswordRequestForm = Depends(),
    x_tenant_domain: str | None = Header(None),
):
    # This endpoint needs to remain public for login

    # Validate tenant
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

    # Find user in that tenant
    user_db = await session.scalar(
        select(User).where(
            (User.email == form_data.username)
            & (User.tenant_id == tenant.id)
            & (User.is_active == True)  # noqa: E712
        )
    )

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, user_db.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    # Include tenant_id in token
    access_token = create_access_token(
        data={
            'sub': user_db.email,
            'tenant_id': str(tenant.id),
            'is_superuser': user_db.is_superuser,
        }
    )

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post(
    '/by-email', status_code=HTTPStatus.OK, response_model=TenantDomainResponse
)
async def get_tenant_domain_by_email(
    email_data: EmailRequest,
    session: T_Session,
):
    """Find tenant domain by user email."""
    user_db = await session.scalar(
        select(User).where(
            (User.email == email_data.email) & (User.is_active == True)  # noqa: E712
        )
    )

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    # Get the tenant for this user
    tenant = await session.scalar(
        select(Tenant).where(
            (Tenant.id == user_db.tenant_id) & (Tenant.is_active == True)  # noqa: E712
        )
    )

    if not tenant:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Tenant not found or inactive',
        )

    # Return as a JSON object instead of a raw string
    return {'domain': tenant.domain}


@router.post('/refresh_token', response_model=Token)
async def refresh_access_token(user: CurrentUser, tenant: CurrentTenant):
    new_access_token = create_access_token(
        data={
            'sub': user.email,
            'tenant_id': str(tenant.id),
            'is_superuser': user.is_superuser,
        }
    )

    return {'access_token': new_access_token, 'token_type': 'bearer'}
