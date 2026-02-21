"""
統合テストモジュール
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """ヘルスチェックテスト"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_api_health():
    """APIヘルスチェックテスト"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_metrics_endpoint():
    """メトリクスエンドポイントテスト"""
    response = client.get("/metrics")
    assert response.status_code == 200


def test_auth_register():
    """ユーザー登録テスト"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 201


def test_auth_login():
    """ログインテスト"""
    # まず登録
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser2",
            "email": "test2@example.com",
            "password": "testpass123"
        }
    )

    # ログイン
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser2",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_protected_endpoint():
    """保護されたエンドポイントのテスト"""
    # ログインしてトークンを取得
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )
    token = login_response.json()["access_token"]

    # 保護されたエンドポイントにアクセス
    response = client.get(
        "/api/v1/services",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_mlops_pipelines():
    """MLOpsパイプラインのテスト"""
    # ログイン
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )
    token = login_response.json()["access_token"]

    # パイプライン一覧取得
    response = client.get(
        "/api/v1/mlops/pipelines",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_data_lake_buckets():
    """データレイクバケットのテスト"""
    # ログイン
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )
    token = login_response.json()["access_token"]

    # バケット一覧取得
    response = client.get(
        "/api/v1/data-lake/buckets",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
