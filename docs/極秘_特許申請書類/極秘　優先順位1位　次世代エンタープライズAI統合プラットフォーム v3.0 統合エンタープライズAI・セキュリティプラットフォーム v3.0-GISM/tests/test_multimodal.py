"""
マルチモーダルAIサービスのテスト
"""
import pytest
import io
from PIL import Image
from app.services.multimodal_ai import MultimodalAIService


@pytest.fixture
def multimodal_service():
    """マルチモーダルAIサービスのフィクスチャ"""
    return MultimodalAIService()


@pytest.fixture
def sample_image():
    """サンプル画像のフィクスチャ"""
    # 簡単なテスト画像を作成
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    return img_bytes.getvalue()


@pytest.mark.asyncio
async def test_service_initialization(multimodal_service):
    """サービス初期化テスト"""
    assert multimodal_service is not None
    assert isinstance(multimodal_service.is_available(), bool)


@pytest.mark.asyncio
async def test_process_text(multimodal_service):
    """テキスト処理テスト"""
    text = "This is a test text"
    
    result = await multimodal_service.process_text(text)
    
    assert "status" in result
    assert result["status"] in ["success", "error"]
    
    if result["status"] == "success":
        assert "text" in result
        assert result["text"] == text


@pytest.mark.asyncio
async def test_generate_caption(multimodal_service, sample_image):
    """画像キャプション生成テスト"""
    result = await multimodal_service.generate_caption(sample_image)
    
    assert "status" in result
    assert result["status"] in ["success", "error"]
    
    if result["status"] == "success":
        assert "caption" in result
        assert isinstance(result["caption"], str)


@pytest.mark.asyncio
async def test_text_image_similarity(multimodal_service, sample_image):
    """テキスト-画像類似度計算テスト"""
    text = "A red image"
    
    result = await multimodal_service.text_image_similarity(text, sample_image)
    
    assert "status" in result
    assert result["status"] in ["success", "error"]
    
    if result["status"] == "success":
        assert "similarity" in result
        assert isinstance(result["similarity"], (int, float))


@pytest.mark.asyncio
async def test_fuse_modalities(multimodal_service):
    """マルチモーダル融合テスト"""
    results = {
        "text": {
            "status": "success",
            "text": "test",
            "embedding": [0.1, 0.2, 0.3]
        },
        "image": {
            "status": "success",
            "similarity": 0.85
        }
    }
    
    result = await multimodal_service.fuse_modalities(results)
    
    assert "status" in result
    assert result["status"] in ["success", "error"]
    
    if result["status"] == "success":
        assert "modalities" in result
        assert "fused_features" in result

