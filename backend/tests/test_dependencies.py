from http import HTTPStatus

import pytest
from fastapi import HTTPException
from jwt import encode

from src.api.dependencies import (
    get_current_active_superuser,
    get_current_user,
    get_tenant_from_domain,
    validate_user_tenant_access,
)
from src.core.settings import settings


@pytest.mark.asyncio
async def test_get_tenant_from_domain_missing_header(session):
    """Test error raised when header is missing"""
    with pytest.raises(HTTPException) as exc_info:
        await get_tenant_from_domain(session, None)

    assert exc_info.value.status_code == HTTPStatus.BAD_REQUEST
    assert 'X-Tenant-Domain header is required' in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_tenant_from_domain_not_found(session):
    """Test error raised when tenant not found"""
    with pytest.raises(HTTPException) as exc_info:
        await get_tenant_from_domain(session, 'non-existent-domain.com')

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert 'Tenant not found or inactive' in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(session, tenant):
    """Test error raised with invalid token"""
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(session, tenant, 'invalid-token')

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_current_user_missing_data(session, tenant):
    """Test error raised when token is missing required data"""
    # Create token without required fields
    token = encode(
        {'some_other_field': 'value'},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(session, tenant, token)

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_current_user_tenant_mismatch(session, tenant, user):
    """Test error raised when token tenant doesn't match request tenant"""
    # Create token with different tenant id
    different_tenant_id = '0' * 32  # Different tenant id
    token = encode(
        {
            'sub': user.email,
            'tenant_id': different_tenant_id,
            'is_superuser': False,
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(session, tenant, token)

    assert exc_info.value.status_code == HTTPStatus.FORBIDDEN
    assert 'Token tenant does not match' in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_current_user_not_found(session, tenant):
    """Test error raised when user not found"""
    # Create token with non-existent user
    token = encode(
        {
            'sub': 'nonexistent@example.com',
            'tenant_id': str(tenant.id),
            'is_superuser': False,
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(session, tenant, token)

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED


def test_get_current_active_superuser_not_superuser(user):
    """Test error raised when user is not superuser"""
    # Ensure user is not a superuser
    user.is_superuser = False

    with pytest.raises(HTTPException) as exc_info:
        get_current_active_superuser(user)

    assert exc_info.value.status_code == HTTPStatus.FORBIDDEN
    assert "doesn't have enough privileges" in exc_info.value.detail


def test_validate_user_tenant_access_superuser(user):
    """Test superuser has access to other users"""
    # Make user a superuser
    user.is_superuser = True

    # This should not raise an exception
    result = validate_user_tenant_access(user, '0' * 32)
    assert result is True


def test_validate_user_tenant_access_self(user):
    """Test user has access to own info"""
    # Make user not a superuser
    user.is_superuser = False

    # This should not raise an exception
    result = validate_user_tenant_access(user, user.id)
    assert result is True


def test_validate_user_tenant_access_denied(user):
    """Test error raised when regular user tries to access other user's info"""
    # Make user not a superuser
    user.is_superuser = False

    with pytest.raises(HTTPException) as exc_info:
        validate_user_tenant_access(user, '0' * 32)

    assert exc_info.value.status_code == HTTPStatus.FORBIDDEN
    assert 'Access denied' in exc_info.value.detail
