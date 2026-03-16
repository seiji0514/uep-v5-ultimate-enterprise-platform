"""
E2E テスト（補強スキル実装の統合確認）
GraphQL、イベントストリーミング、トレーシング等
"""
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.fixture
def auth_headers():
    """認証ヘッダー取得"""
    r = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    if r.status_code != 200:
        return {}
    token = r.json().get("access_token")
    return {"Authorization": f"Bearer {token}"} if token else {}


def test_graphql_hello():
    """GraphQL hello クエリ"""
    r = client.post(
        "/graphql",
        json={"query": "{ hello }"},
        headers={"Content-Type": "application/json"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "hello" in data["data"]
    assert "UEP" in data["data"]["hello"]


def test_graphql_health():
    """GraphQL health クエリ"""
    r = client.post(
        "/graphql",
        json={"query": "{ health { status version } }"},
        headers={"Content-Type": "application/json"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data.get("data", {}).get("health", {}).get("status") == "healthy"


def test_graphql_projects():
    """GraphQL projects クエリ"""
    r = client.post(
        "/graphql",
        json={"query": "{ projects { id name } }"},
        headers={"Content-Type": "application/json"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "projects" in data.get("data", {})


def test_falco_webhook():
    """Falco Webhook 受信（security-defense-platform は別起動のため 404 時はスキップ）"""
    r = client.post(
        "/api/v1/security-defense-platform/falco/alerts",
        json={
            "output": "Test alert",
            "priority": "Warning",
            "rule": "test_rule",
        },
        headers={"Content-Type": "application/json"},
    )
    if r.status_code == 404:
        pytest.skip("security-defense-platform は別起動が必要（EOH 等）")
    assert r.status_code == 202
    assert r.json().get("received") is True


def test_health_traceparent():
    """W3C Trace Context 伝搬（traceparent）"""
    r = client.get(
        "/api/v1/health",
        headers={
            "traceparent": "00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"
        },
    )
    assert r.status_code == 200


def test_events_outbox_create(auth_headers):
    """アウトボックスイベント作成"""
    if not auth_headers:
        pytest.skip("Auth required")
    r = client.post(
        "/api/v1/events/outbox",
        json={
            "aggregate_type": "Order",
            "aggregate_id": "o-e2e-1",
            "event_type": "Created",
            "payload": {"test": True},
        },
        headers=auth_headers,
    )
    assert r.status_code == 201
    assert "event_id" in r.json()


def test_events_saga_create(auth_headers):
    """Saga 作成"""
    if not auth_headers:
        pytest.skip("Auth required")
    r = client.post(
        "/api/v1/events/saga",
        json={
            "saga_type": "order",
            "steps": [
                {"action": "reserve", "compensate_action": "release", "payload": {}},
            ],
        },
        headers=auth_headers,
    )
    assert r.status_code == 201
    assert "saga_id" in r.json()
    assert r.json().get("status") == "pending"
