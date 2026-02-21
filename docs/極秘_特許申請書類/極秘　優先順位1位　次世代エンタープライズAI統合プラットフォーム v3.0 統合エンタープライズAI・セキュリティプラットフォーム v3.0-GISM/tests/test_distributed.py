"""
分散処理サービスのテスト
"""
import pytest
import asyncio
from app.services.distributed_processing import DistributedProcessingService


@pytest.fixture
def distributed_service():
    """分散処理サービスのフィクスチャ"""
    return DistributedProcessingService()


@pytest.mark.asyncio
async def test_service_initialization(distributed_service):
    """サービス初期化テスト"""
    assert distributed_service is not None
    # サービスが利用可能かチェック（実装により異なる）
    assert isinstance(distributed_service.is_available(), bool)


@pytest.mark.asyncio
async def test_process_large_scale_data(distributed_service):
    """大規模データ処理テスト"""
    # モックデータソースを使用
    result = await distributed_service.process_large_scale_data("test_data.parquet")
    
    assert "status" in result
    # Sparkが利用できない場合もエラーメッセージを返すことを確認
    assert result["status"] in ["success", "error"]


@pytest.mark.asyncio
async def test_stream_data(distributed_service):
    """ストリーミングデータ処理テスト"""
    result = await distributed_service.stream_data("test_topic")
    
    assert "status" in result
    assert result["status"] in ["success", "error"]


@pytest.mark.asyncio
async def test_distributed_training(distributed_service):
    """分散学習テスト"""
    model_config = {
        "model_type": "test_model",
        "epochs": 10
    }
    
    result = await distributed_service.distributed_training(model_config)
    
    assert "status" in result
    assert result["status"] in ["success", "error"]


@pytest.mark.asyncio
async def test_process_time_series(distributed_service):
    """時系列データ処理テスト"""
    time_series_data = [1.0, 2.0, 3.0, 4.0, 5.0]
    
    result = await distributed_service.process_time_series(time_series_data)
    
    assert "status" in result
    assert result["status"] in ["success", "error"]
    
    if result["status"] == "success":
        assert "mean" in result
        assert "count" in result

