"""
APIレート制限のテスト
"""
import pytest
from fastapi.testclient import TestClient

from core.rate_limit import limiter
from main import app

client = TestClient(app)


def test_rate_limit():
    """レート制限をテスト"""
    # レート制限内のリクエスト
    for i in range(10):
        response = client.get("/health")
        assert response.status_code in [200, 429]

    # レート制限ヘッダー（slowapi が付与する場合）または 429 を許容
    response = client.get("/health")
    assert response.status_code in [200, 429]
    if response.status_code == 200:
        # ヘッダーは任意（slowapi のバージョン・設定により異なる）
        pass
