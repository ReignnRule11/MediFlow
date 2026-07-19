"""
tests/test_auth.py - Authentication tests
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.dependencies import get_db
from app.models import Base, User, UserRole
from app.core.security import hash_password

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override get_db for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture
def test_user_data():
    """Test user data"""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "full_name": "Test User"
    }


@pytest.fixture
def test_user(test_user_data):
    """Create test user"""
    db = TestingSessionLocal()
    user = User(
        email=test_user_data["email"],
        full_name=test_user_data["full_name"],
        hashed_password=hash_password(test_user_data["password"]),
        role=UserRole.PATIENT,
        is_active=True,
        email_verified=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


def test_signup(test_user_data):
    """Test user signup"""
    response = client.post("/auth/signup", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"]
    assert data["refresh_token"]
    assert data["token_type"] == "bearer"


def test_signup_duplicate_email(test_user, test_user_data):
    """Test signup with duplicate email"""
    response = client.post("/auth/signup", json=test_user_data)
    assert response.status_code == 409


def test_signup_weak_password():
    """Test signup with weak password"""
    weak_password_user = {
        "email": "newuser@example.com",
        "password": "weak",
        "full_name": "Test User"
    }
    response = client.post("/auth/signup", json=weak_password_user)
    assert response.status_code == 422


def test_login(test_user, test_user_data):
    """Test user login"""
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"]
    assert data["refresh_token"]


def test_login_wrong_password(test_user, test_user_data):
    """Test login with wrong password"""
    login_data = {
        "email": test_user_data["email"],
        "password": "WrongPassword123!"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401


def test_login_nonexistent_user():
    """Test login with nonexistent user"""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "Password123!"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401


def test_refresh_token(test_user, test_user_data):
    """Test token refresh"""
    # First login
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    login_response = client.post("/auth/login", json=login_data)
    refresh_token = login_response.json()["refresh_token"]

    # Refresh the token
    refresh_data = {"refresh_token": refresh_token}
    response = client.post("/auth/refresh", json=refresh_data)
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
