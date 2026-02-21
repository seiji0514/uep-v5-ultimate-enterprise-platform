"""
APIレート制限のテスト
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from core.rate_limit import limiter


client = TestClient(app)


def test_rate_limit():
    """レート制限をテスト"""
    # レート制限内のリクエスト
    for i in range(10):
        response = client.get("/health")
        assert response.status_code in [200, 429]

    # レート制限ヘッダーの確認
    response = client.get("/health")
    assert "X-RateLimit-Limit" in response.headers or response.status_code == 429
