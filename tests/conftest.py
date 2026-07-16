from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from apps.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest
from apps.main import app
from apps.database import Base, get_db
from apps.oauth2 import create_access_token
from apps import models


SQLALCHEMY_DB_URL = 'postgresql://postgres:ahmad%40512@localhost:5432/fastapi_test'

# SQLALCHEMY_DB_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{se ttings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DB_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
                
Base.metadata.create_all(bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "ahmad@gmail.com", "password": "ahmad123"}
    res = client.post("/users/", json=user_data)

    new_user = res.json()
    new_user['password'] = user_data['password']
    
    assert res.status_code == 201

    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user['id']
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "owner_id": test_user['id']
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user['id']
        },
        {
            "title": "4th title",
            "content": "4th content",
            "owner_id": test_user2['id']
        }
    ]

    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)

    session.commit()

    all_posts = session.query(models.Post).all()

    return all_posts

@pytest.fixture
def test_user2(client):
    user_data = {"email": "ahmad12@gmail.com", "password": "ahmad123"}
    res = client.post("/users/", json=user_data)

    new_user = res.json()
    new_user['password'] = user_data['password']
    
    assert res.status_code == 201

    return new_user