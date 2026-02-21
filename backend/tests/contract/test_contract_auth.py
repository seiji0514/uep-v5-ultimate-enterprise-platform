"""
Contract Testing - 認証API
フロントエンドとバックエンド間のAPI契約を検証する
"""
import pytest
from fastapi.testclient import TestClient


# conftest.py で app を取得するため、fixture を定義
@pytest.fixture
def client():
    """TestClient を取得"""
    from main import app
    return TestClient(app)


@pytest.fixture
def auth_token(client: TestClient) -> str:
    """認証トークンを取得"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "developer", "password": "dev123"},
    )
    assert response.status_code == 200
    data = response.json()
    return data["access_token"]


class TestAuthLoginContract:
    """POST /api/v1/auth/login の契約テスト"""

    def test_login_returns_required_fields(self, client: TestClient):
        """ログインAPIが契約で定義された必須フィールドを返すこと"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "developer", "password": "dev123"},
        )
        assert response.status_code == 200
        data = response.json()

        # 契約: access_token, token_type, expires_in, user が必須
        assert "access_token" in data
        assert isinstance(data["access_token"], str)
        assert len(data["access_token"]) > 0

        assert data.get("token_type") == "bearer"
        assert "expires_in" in data
        assert isinstance(data["expires_in"], int)

        assert "user" in data
        user = data["user"]
        assert "username" in user
        assert "email" in user
        assert "roles" in user
        assert isinstance(user["roles"], list)
        assert "is_active" in user
        assert isinstance(user["is_active"], bool)

    def test_login_rejects_invalid_credentials(self, client: TestClient):
        """無効な認証情報で401を返すこと"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "invalid", "password": "wrong"},
        )
        assert response.status_code == 401
        data = response.json()
        # 契約: エラー情報（detail または error.message）が含まれること
        assert "detail" in data or ("error" in data and "message" in data["error"])


class TestAuthMeContract:
    """GET /api/v1/auth/me の契約テスト"""

    def test_me_returns_user_info_with_valid_token(
        self, client: TestClient, auth_token: str
    ):
        """有効なトークンでユーザー情報を返すこと"""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 200
        data = response.json()

        # 契約: username, email, roles, permissions, is_active が必須
        assert "username" in data
        assert "email" in data
        assert "roles" in data
        assert isinstance(data["roles"], list)
        assert "permissions" in data
        assert isinstance(data["permissions"], list)
        assert "is_active" in data

    def test_me_rejects_invalid_token(self, client: TestClient):
        """無効なトークンで401を返すこと"""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid-token"},
        )
        assert response.status_code == 401


class TestHealthContract:
    """GET /health の契約テスト"""

    def test_health_returns_required_fields(self, client: TestClient):
        """ヘルスチェックが契約で定義されたフィールドを返すこと"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()

        assert data.get("status") == "healthy"
        assert "version" in data
        assert "service" in data
