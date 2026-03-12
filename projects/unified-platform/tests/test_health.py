"""Phase 4: CI - Health check test"""
import os
os.environ["TESTING"] = "true"
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "Unified Platform" in r.json()["service"]


def test_login():
    r = client.post("/api/v1/auth/login", data={"username": "admin", "password": "admin"})
    assert r.status_code == 200
    assert "access_token" in r.json()
