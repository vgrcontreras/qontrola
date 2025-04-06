from unittest import mock

import pytest

from src.core.database import init_db
from src.core.settings import settings
from src.models import Tenant, User


@pytest.mark.asyncio
async def test_init_db_superuser_exists(session):
    """Test init_db when superuser already exists"""
    # Create a tenant for the superuser
    tenant = Tenant(name='test-tenant', domain='test-domain.com')
    session.add(tenant)
    await session.commit()

    # Create a superuser first
    user = User(
        full_name='existing admin',
        email=settings.FIRST_SUPERUSER_EMAIL,
        password='hashed_password',
        is_superuser=True,
        tenant_id=tenant.id,
        tenant=tenant,
    )
    session.add(user)
    await session.commit()

    # Now run init_db
    result = await init_db(session)

    # Should return the existing user
    assert result.email == settings.FIRST_SUPERUSER_EMAIL
    assert result.full_name == 'existing admin'


@pytest.mark.asyncio
async def test_init_db_create_superuser(session):
    """Test init_db creates superuser when it doesn't exist"""
    # Mock the password hash function to avoid actual hashing
    with mock.patch(
        'src.core.database.get_password_hash', return_value='mocked_hash'
    ):
        # Run init_db function which should create both tenant and user
        result = await init_db(session)

    # Verify a superuser was created
    assert result is not None
    assert result.email == settings.FIRST_SUPERUSER_EMAIL
    assert result.is_superuser is True

    # Verify tenant_id exists (without accessing the tenant relationship)
    assert result.tenant_id is not None
