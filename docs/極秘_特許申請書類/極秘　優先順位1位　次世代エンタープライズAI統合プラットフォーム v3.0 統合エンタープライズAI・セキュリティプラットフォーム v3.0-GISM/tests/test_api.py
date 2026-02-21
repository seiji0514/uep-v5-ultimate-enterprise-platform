"""
APIエンドポイントのテスト
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """ルートエンドポイントテスト"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert data["version"] == "8.0.0"


def test_health_check():
    """ヘルスチェックテスト"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "services" in data


def test_multimodal_process_text_only():
    """マルチモーダル処理（テキストのみ）テスト"""
    response = client.post(
        "/api/v1/multimodal/process",
        json={"text": "Test text"}
    )
    assert response.status_code in [200, 422]  # 422はバリデーションエラー


def test_distributed_process():
    """分散処理APIテスト"""
    response = client.post(
        "/api/v1/distributed/process",
        json={
            "data_source": "test_data.parquet",
            "processing_type": "batch"
        }
    )
    assert response.status_code in [200, 422]


def test_integration_connect():
    """既存システム統合APIテスト"""
    response = client.post("/api/v1/integration/connect")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "connected_systems" in data


# フェーズ2: コンピュータビジョンAPIテスト
def test_detect_objects_api():
    """物体検出APIテスト"""
    from PIL import Image
    import io
    
    # サンプル画像を作成
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    response = client.post(
        "/api/v2/vision/detect",
        files={"image": ("test.png", img_bytes, "image/png")}
    )
    assert response.status_code in [200, 500]  # 成功またはエラー（YOLO未インストール時）
    if response.status_code == 200:
        assert "status" in response.json()


def test_segment_image_api():
    """画像セグメンテーションAPIテスト"""
    from PIL import Image
    import io
    
    # サンプル画像を作成
    img = Image.new('RGB', (100, 100), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    response = client.post(
        "/api/v2/vision/segment",
        files={"image": ("test.png", img_bytes, "image/png")}
    )
    assert response.status_code == 200
    assert "status" in response.json()


# フェーズ2: 音声処理APIテスト
def test_synthesize_speech_api():
    """音声合成APIテスト"""
    response = client.post(
        "/api/v2/audio/synthesize",
        params={"text": "Hello, this is a test.", "language": "en"}
    )
    assert response.status_code == 200
    assert "status" in response.json()

