"""
Contract Testing - Chaos Engineering API
Chaos UI とバックエンド間のAPI契約を検証する
"""
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """TestClient を取得"""
    from main import app
    return TestClient(app)


class TestChaosStatusContract:
    """GET /api/v1/chaos/status の契約テスト"""

    def test_chaos_status_returns_required_fields(self, client: TestClient):
        """Chaos status APIが契約で定義された必須フィールドを返すこと"""
        response = client.get("/api/v1/chaos/status")
        assert response.status_code == 200
        data = response.json()

        assert "enabled" in data
        assert isinstance(data["enabled"], bool)
        assert "endpoints" in data
        assert "delay" in data["endpoints"]
        assert "error" in data["endpoints"]
        assert "mixed" in data["endpoints"]
        assert "description" in data


class TestChaosDelayContract:
    """GET /api/v1/chaos/delay の契約テスト"""

    def test_chaos_delay_returns_required_fields(self, client: TestClient):
        """遅延注入APIが契約で定義されたフィールドを返すこと"""
        response = client.get("/api/v1/chaos/delay?delay_ms=10&jitter_ms=0")
        assert response.status_code == 200
        data = response.json()

        assert "status" in data
        assert data["status"] == "ok"
        assert "message" in data
        assert "requested_delay_ms" in data
        assert "actual_delay_ms" in data
        assert data["requested_delay_ms"] == 10
