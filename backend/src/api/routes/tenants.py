from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import (
    CurrentTenant,
    T_Session,
    get_current_active_superuser,
)
from src.models import Tenant, User
from src.schemas.tenants import TenantPublic, TenantRegistration, TenantUpdate
from src.security import get_password_hash

router = APIRouter()


@router.post(
    '/register', status_code=HTTPStatus.CREATED, response_model=TenantPublic
)
async def register_tenant(
    tenant_registration: TenantRegistration, session: T_Session
):
    """
    Register a new tenant and create the first admin user.
    This endpoint is public and doesn't require authentication.
    """
    try:
        # First check if domain is available
        existing_tenant = await session.scalar(
            select(Tenant).where(Tenant.domain == tenant_registration.domain)
        )

        if existing_tenant:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Domain already in use',
            )

        # Create the tenant
        new_tenant = Tenant(
            name=tenant_registration.name,
            domain=tenant_registration.domain,
        )

        session.add(new_tenant)

        # Flush to get the tenant ID
        await session.flush()

        # Create the admin user
        admin_data = tenant_registration.admin_user
        hashed_password = get_password_hash(admin_data.password)

        admin_user = User(
            email=admin_data.email,
            password=hashed_password,
            is_superuser=True,
            tenant=new_tenant,
            tenant_id=new_tenant.id,
        )

        session.add(admin_user)

        await session.commit()
        return new_tenant

    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Error creating tenant: {str(e)}',
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Unexpected error: {str(e)}',
        )


@router.put(
    '/current',
    dependencies=[Depends(get_current_active_superuser)],
    response_model=TenantPublic,
)
async def update_tenant(
    tenant_update: TenantUpdate,
    tenant: CurrentTenant,
    session: T_Session,
):
    """
    Update tenant information. Only accessible by tenant administrators.
    """
    # Apply updates to fields that are provided
    if tenant_update.name is not None:
        tenant.name = tenant_update.name

    if tenant_update.domain is not None:
        # Check if domain is available
        if tenant_update.domain != tenant.domain:
            existing_tenant = await session.scalar(
                select(Tenant).where(Tenant.domain == tenant_update.domain)
            )

            if existing_tenant:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f'Domain {tenant_update.domain} is already in use',
                )

            tenant.domain = tenant_update.domain

    if tenant_update.is_active is not None:
        tenant.is_active = tenant_update.is_active

    session.add(tenant)
    await session.commit()
    await session.refresh(tenant)

    return tenant
