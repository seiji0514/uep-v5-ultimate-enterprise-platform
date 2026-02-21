"""
既存システム統合サービスのテスト
"""
import pytest
from app.services.integration import IntegrationService


@pytest.fixture
def integration_service():
    """既存システム統合サービスのフィクスチャ"""
    return IntegrationService()


@pytest.mark.asyncio
async def test_service_initialization(integration_service):
    """サービス初期化テスト"""
    assert integration_service is not None
    assert integration_service.is_available() is True


@pytest.mark.asyncio
async def test_connect_existing_systems(integration_service):
    """既存システム接続テスト"""
    result = await integration_service.connect_existing_systems()
    
    assert "connected" in result
    assert "failed" in result
    assert "systems" in result
    assert isinstance(result["connected"], list)
    assert isinstance(result["failed"], list)


@pytest.mark.asyncio
async def test_call_existing_system(integration_service):
    """既存システムAPI呼び出しテスト"""
    # 存在しないシステムIDの場合
    result = await integration_service.call_existing_system(
        "nonexistent_system",
        "/test"
    )
    
    assert "status" in result
    assert result["status"] == "error"

