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


