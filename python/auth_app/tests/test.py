from fastapi.testclient import TestClient
from python.auth_app.auth import app

client = TestClient(app)

def test_login_success():
    response = client.post("/login", json={
        "username": "admin",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_fail():
    response = client.post("/login", json={
        "username": "admin",
        "password": "adm"
    })
    assert response.status_code == 401