from http import HTTPStatus

import pytest
from fastapi import HTTPException
from jwt import encode

from src.api.dependencies import (
    get_current_active_superuser,
    get_current_user,
    validate_user_access,
)
from src.core.settings import settings


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(session):
    """Test error raised with invalid token"""
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(session, 'invalid-token')

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_current_user_missing_data(session):
    """Test error raised when token is missing required data"""
    # Create token without required fields
    token = encode(
        {'some_other_field': 'value'},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(session, token)

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_current_user_not_found(session):
    """Test error raised when user not found"""
    # Create token with non-existent user
    token = encode(
        {
            'sub': 'nonexistent@example.com',
            'is_superuser': False,
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(session, token)

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED


def test_get_current_active_superuser_not_superuser(user):
    """Test error raised when user is not superuser"""
    # Ensure user is not a superuser
    user.is_superuser = False

    with pytest.raises(HTTPException) as exc_info:
        get_current_active_superuser(user)

    assert exc_info.value.status_code == HTTPStatus.FORBIDDEN
    assert "doesn't have enough privileges" in exc_info.value.detail


def test_validate_user_access_superuser(user):
    """Test superuser has access to other users"""
    # Make user a superuser
    user.is_superuser = True

    # This should not raise an exception
    result = validate_user_access(user, '0' * 32)
    assert result is True


def test_validate_user_access_self(user):
    """Test user has access to own info"""
    # Make user not a superuser
    user.is_superuser = False

    # This should not raise an exception
    result = validate_user_access(user, user.id)
    assert result is True


def test_validate_user_access_denied(user):
    """Test error raised when regular user tries to access other user's info"""
    # Make user not a superuser
    user.is_superuser = False

    with pytest.raises(HTTPException) as exc_info:
        validate_user_access(user, '0' * 32)

    assert exc_info.value.status_code == HTTPStatus.FORBIDDEN
    assert 'Access denied' in exc_info.value.detail
