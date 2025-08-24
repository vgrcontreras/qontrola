from contextlib import contextmanager
from datetime import date, datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from src.api.dependencies import get_session
from src.api.main import app
from src.models import Client, Project, User, table_registry
from src.security import get_password_hash


@pytest_asyncio.fixture
def api_client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
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
async def user(session):
    password = 'test_password'

    user = User(
        full_name='test',
        email='test@test.com',
        password=get_password_hash(password),
        is_superuser=False,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest_asyncio.fixture
async def superuser(session):
    password = 'admin'

    super_user = User(
        full_name='admin',
        email='admin@admin.com',
        password=get_password_hash(password),
        is_superuser=True,
    )

    session.add(super_user)
    await session.commit()
    await session.refresh(super_user)

    super_user.clean_password = password

    return super_user


@pytest_asyncio.fixture
async def db_client(session):
    client_db = Client(
        name='test',
        client_type='test',
        type_identifier='cnpj',
        identifier='12345678901234',
    )

    session.add(client_db)
    await session.commit()
    await session.refresh(client_db)

    return client_db


@pytest_asyncio.fixture
async def db_project(session, superuser):
    project = Project(
        name='test_project',
        status_state='active',
        project_value=1000.0,
        target_date=date(2024, 12, 31),
        created_by=superuser.id,
        is_active=True,
    )
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


@pytest_asyncio.fixture
def user_token(api_client, user):
    response = api_client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
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
    )

    return response.json()['access_token']
