"""
APIエンドポイントの包括的なテスト
"""
import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_health_check():
    """ヘルスチェックエンドポイントをテスト"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_api_health():
    """APIヘルスチェックエンドポイントをテスト"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_metrics_endpoint():
    """メトリクスエンドポイントをテスト"""
    response = client.get("/metrics")
    assert response.status_code == 200


def test_openapi_docs():
    """OpenAPIドキュメントエンドポイントをテスト"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_json():
    """OpenAPI JSONエンドポイントをテスト"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()


def test_404_error():
    """404エラーハンドリングをテスト"""
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert "error" in response.json()


def test_error_response_format():
    """エラーレスポンスの形式をテスト"""
    response = client.get("/nonexistent")
    error = response.json()["error"]
    assert "code" in error
    assert "message" in error
    assert "path" in error
    assert "timestamp" in error
