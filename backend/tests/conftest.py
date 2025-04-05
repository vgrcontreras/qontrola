from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from src.api.dependencies import get_session, get_tenant_from_domain
from src.api.main import app
from src.models import Client, Tenant, User, table_registry
from src.security import get_password_hash


@pytest_asyncio.fixture
def api_client(session, tenant):
    def get_session_override():
        return session

    def get_tenant_override():
        return tenant

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        app.dependency_overrides[get_tenant_from_domain] = get_tenant_override

        # For debugging - add a tenant domain header to all requests
        original_request = client.request

        def request_with_tenant_header(method, url, **kwargs):
            if 'headers' not in kwargs or kwargs['headers'] is None:
                kwargs['headers'] = {}

            if (
                isinstance(kwargs['headers'], dict)
                and tenant is not None
                and hasattr(tenant, 'domain')
            ):
                kwargs['headers']['X-Tenant-Domain'] = tenant.domain

            return original_request(method, url, **kwargs)

        client.request = request_with_tenant_header

        yield client

    app.dependency_overrides.clear()


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest_asyncio.fixture
async def tenant(session):
    tenant = Tenant(name='test-tenant', domain='test-domain.com')

    session.add(tenant)
    await session.commit()
    await session.refresh(tenant)

    return tenant


@pytest_asyncio.fixture
async def user(session, tenant):
    password = 'test_password'

    # Note: we need to pass both tenant and tenant_id due to SQLAlchemy's
    # mapper configuration
    user = User(
        first_name='test',
        last_name='test',
        email='test@test.com',
        password=get_password_hash(password),
        is_superuser=False,
        tenant_id=tenant.id,
        tenant=tenant,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest_asyncio.fixture
async def superuser(session, tenant):
    password = 'admin'

    # Note: we need to pass both tenant and tenant_id due to SQLAlchemy's
    # mapper configuration
    super_user = User(
        first_name='admin',
        last_name='admin',
        email='admin@admin.com',
        password=get_password_hash(password),
        is_superuser=True,
        tenant_id=tenant.id,
        tenant=tenant,
    )

    session.add(super_user)
    await session.commit()
    await session.refresh(super_user)

    super_user.clean_password = password

    return super_user


@pytest_asyncio.fixture
async def db_client(session, tenant):
    # Note: we need to pass both tenant and tenant_id due to SQLAlchemy's
    # mapper configuration
    client_db = Client(
        name='test',
        client_type='test',
        type_identifier='cnpj',
        identifier='test',
        tenant_id=tenant.id,
        tenant=tenant,
    )

    session.add(client_db)
    await session.commit()
    await session.refresh(client_db)

    return client_db


@pytest_asyncio.fixture
def user_token(api_client, user):
    response = api_client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
        headers={'X-Tenant-Domain': user.tenant.domain},
    )

    return response.json()['access_token']


@pytest_asyncio.fixture
def superuser_token(api_client, superuser):
    response = api_client.post(
        '/token',
        data={
            'username': superuser.email,
            'password': superuser.clean_password,
        },
        headers={'X-Tenant-Domain': superuser.tenant.domain},
    )

    return response.json()['access_token']
