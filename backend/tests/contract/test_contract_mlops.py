"""
Contract Testing - MLOps API
フロントエンドとバックエンド間のMLOps API契約を検証する
"""
import pytest
from fastapi.testclient import TestClient


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


class TestMLOpsPipelinesContract:
    """GET /api/v1/mlops/pipelines の契約テスト"""

    def test_pipelines_returns_array(self, client: TestClient, auth_token: str):
        """パイプライン一覧が配列を返すこと"""
        response = client.get(
            "/api/v1/mlops/pipelines",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestMLOpsModelsContract:
    """GET /api/v1/mlops/models の契約テスト"""

    def test_models_returns_array(self, client: TestClient, auth_token: str):
        """モデル一覧が配列を返すこと"""
        response = client.get(
            "/api/v1/mlops/models",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
