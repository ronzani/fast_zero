# import factory
import factory.fuzzy
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import ToDo, ToDoState, User, table_registry
from fast_zero.schemas import UserPublicSchema
from fast_zero.security import get_password_hash


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())

        yield _engine


@pytest.fixture()
def session(engine):
    # engine = create_engine(
    #     'sqlite:///:memory:',
    #     connect_args={'check_same_thread': False},
    #     poolclass=StaticPool,
    # )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}123')


@pytest.fixture()
def user(session):
    password = 'test@123'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture()
def other_user(session):
    _user = UserFactory()

    session.add(_user)
    session.commit()
    session.refresh(_user)

    return _user


@pytest.fixture()
def user_public_schema(user):
    return UserPublicSchema.model_validate(user).model_dump()


@pytest.fixture()
def token(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )
    return response.json()['access_token']


@pytest.fixture()
def header_authorization(token):
    return {'Authorization': f'Bearer {token}'}


class ToDoFactory(factory.Factory):
    class Meta:
        model = ToDo

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(ToDoState)
    user_id = 1
