"""
セキュリティ機能のテスト
"""
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_security_headers():
    """セキュリティヘッダーをテスト"""
    response = client.get("/health")

    assert "X-Content-Type-Options" in response.headers
    assert "X-Frame-Options" in response.headers
    assert "X-XSS-Protection" in response.headers
    assert response.headers["X-Frame-Options"] == "DENY"


def test_cors_headers():
    """CORSヘッダーをテスト"""
    response = client.options("/health", headers={"Origin": "http://localhost:3000"})

    assert response.status_code == 200
