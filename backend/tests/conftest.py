import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.api.dependencies import get_session
from src.api.main import app
from src.models import Client, User, table_registry
from src.security import get_password_hash


@pytest.fixture
def api_client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    password = 'test_password'

    user = User(
        first_name='test',
        last_name='test',
        email='test@test.com',
        password=get_password_hash(password),
        is_superuser=False,
        salary=1000,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def superuser(session):
    password = 'admin'

    super_user = User(
        first_name='admin',
        last_name='admin',
        email='admin@admin.com',
        password=get_password_hash(password),
        is_superuser=True,
        salary=0,
    )

    session.add(super_user)
    session.commit()
    session.refresh(super_user)

    super_user.clean_password = password

    return super_user


@pytest.fixture
def db_client(session):
    client_db = Client(
        name='test',
        client_type='test',
        type_identifier='cnpj',
        identifier='test',
    )

    session.add(client_db)
    session.commit()
    session.refresh(client_db)

    return client_db


@pytest.fixture
def user_token(api_client, user):
    response = api_client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']


@pytest.fixture
def superuser_token(api_client, superuser):
    response = api_client.post(
        '/token',
        data={
            'username': superuser.email,
            'password': superuser.clean_password,
        },
    )

    return response.json()['access_token']
