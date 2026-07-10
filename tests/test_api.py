import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ==========================================
# AUTH TESTS
# ==========================================

def test_signup_creates_user():
    response = client.post(
        "/auth/signup",
        json={"username": "testuser1", "password": "testpass123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser1"
    # Making sure the password is NEVER returned in the response
    assert "password" not in data
    assert "hashed_password" not in data


def test_signup_duplicate_username_fails():
    client.post("/auth/signup", json={"username": "dupuser", "password": "pass123"})
    response = client.post("/auth/signup", json={"username": "dupuser", "password": "pass456"})
    assert response.status_code == 400


def test_login_with_correct_credentials():
    client.post("/auth/signup", json={"username": "loginuser", "password": "mypassword"})
    response = client.post(
        "/auth/login",
        data={"username": "loginuser", "password": "mypassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_with_wrong_password_fails():
    client.post("/auth/signup", json={"username": "wrongpassuser", "password": "correctpass"})
    response = client.post(
        "/auth/login",
        data={"username": "wrongpassuser", "password": "incorrectpass"},
    )
    assert response.status_code == 401


# ==========================================
# STUDENT TESTS
# ==========================================

def get_auth_token():
    """Helper: signs up + logs in a fresh user, returns an access token."""
    client.post("/auth/signup", json={"username": "studentmgr", "password": "pass123"})
    response = client.post(
        "/auth/login",
        data={"username": "studentmgr", "password": "pass123"},
    )
    return response.json()["access_token"]


def test_create_student_requires_auth():
    # No Authorization header sent -> should be rejected
    response = client.post(
        "/students/",
        json={"name": "Alice", "age": 20, "year": "2nd"},
    )
    assert response.status_code == 401


def test_create_student_with_auth_succeeds():
    token = get_auth_token()
    response = client.post(
        "/students/",
        json={"name": "Bob", "age": 21, "year": "3rd"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Bob"


def test_get_all_students_is_public():
    # No token needed for reading
    response = client.get("/students/")
    assert response.status_code == 200


def test_get_nonexistent_student_returns_404():
    response = client.get("/students/99999")
    assert response.status_code == 404
