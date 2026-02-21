"""
統合プラットフォームの統合テスト
v3.0: v2.0 (MLOps) + v8.0 (マルチモーダルAI)
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import httpx
from fastapi.testclient import TestClient

# テスト用のインポート
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)


class TestIntegratedPlatform:
    """統合プラットフォームのテスト"""
    
    def test_root_endpoint(self):
        """ルートエンドポイントのテスト"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "次世代エンタープライズAI統合プラットフォーム v3.0"
        assert data["version"] == "3.0.0"
        assert "mlops" in data["features"]
        assert "multimodal_ai" in data["features"]
    
    def test_health_check(self):
        """ヘルスチェックのテスト"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "services" in data
        assert "quantum_optimizer" in data["services"]
        assert "adaptive_fusion" in data["services"]
    
    @pytest.mark.asyncio
    async def test_quantum_optimize_api(self):
        """量子最適化APIのテスト"""
        request_data = {
            "locations": [
                {"latitude": 35.6762, "longitude": 139.6503, "weight": 1.0},
                {"latitude": 35.6812, "longitude": 139.6553, "weight": 1.0},
                {"latitude": 35.6712, "longitude": 139.6453, "weight": 1.0}
            ],
            "num_select": 2
        }
        
        response = client.post("/api/v3/mlops/quantum-optimize", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "selected_locations" in data
        assert "speedup" in data
    
    @pytest.mark.asyncio
    async def test_homomorphic_fl_api(self):
        """準同型暗号FL APIのテスト"""
        request_data = {
            "client_models": [
                {"client_id": "client1", "weights": [0.1, 0.2, 0.3]},
                {"client_id": "client2", "weights": [0.2, 0.3, 0.4]}
            ],
            "aggregation_method": "fedavg"
        }
        
        response = client.post("/api/v3/mlops/homomorphic-fl", json=request_data)
        # サービスが利用可能でない場合は503を期待
        assert response.status_code in [200, 503]
    
    def test_self_healing_status_api(self):
        """自己修復ステータスAPIのテスト"""
        response = client.get("/api/v3/mlops/self-healing/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "incident_summary" in data
    
    @pytest.mark.asyncio
    async def test_multi_cloud_optimize_api(self):
        """マルチクラウド最適化APIのテスト"""
        request_data = {
            "workload_size": 100.0,
            "user_location": [35.6762, 139.6503],
            "cost_weight": 0.4,
            "latency_weight": 0.4,
            "availability_weight": 0.2
        }
        
        response = client.post("/api/v3/mlops/multi-cloud/optimize", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "recommended_provider" in data
    
    @pytest.mark.asyncio
    async def test_quantum_optimized_fusion_api(self):
        """量子最適化マルチモーダル融合APIのテスト"""
        request_data = {
            "modality_results": [
                {
                    "modality": "text",
                    "data": {"text": "test"},
                    "confidence": 0.8,
                    "metadata": {}
                },
                {
                    "modality": "image",
                    "data": {"image": "test"},
                    "confidence": 0.9,
                    "metadata": {}
                }
            ],
            "strategy": "context_aware"
        }
        
        response = client.post("/api/v3/integrated/quantum-optimized-fusion", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "fusion_result" in data
    
    @pytest.mark.asyncio
    async def test_secure_multimodal_api(self):
        """準同型暗号マルチモーダル処理APIのテスト"""
        # テキストのみのテスト
        request_data = {
            "text": "test text",
            "encrypt": True
        }
        
        response = client.post("/api/v3/integrated/secure-multimodal", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "privacy_protected" in data


class TestMLOpsServices:
    """MLOpsサービスのテスト"""
    
    def test_quantum_optimizer_initialization(self):
        """量子最適化サービスの初期化テスト"""
        from app.services.mlops import QuantumGeospatialOptimizer
        optimizer = QuantumGeospatialOptimizer()
        assert optimizer is not None
    
    def test_self_healing_initialization(self):
        """自己修復サービスの初期化テスト"""
        from app.services.mlops import SelfHealingOrchestrator
        orchestrator = SelfHealingOrchestrator()
        assert orchestrator is not None
    
    def test_multi_cloud_initialization(self):
        """マルチクラウドサービスの初期化テスト"""
        from app.services.mlops import MultiCloudManager
        manager = MultiCloudManager()
        assert manager is not None


class TestMultimodalServices:
    """マルチモーダルAIサービスのテスト"""
    
    def test_adaptive_fusion_initialization(self):
        """適応的融合エンジンの初期化テスト"""
        from app.core.adaptive_fusion import AdaptiveMultimodalFusion
        fusion_engine = AdaptiveMultimodalFusion()
        assert fusion_engine is not None
    
    def test_adaptive_cache_initialization(self):
        """適応的キャッシュの初期化テスト"""
        from app.core.adaptive_cache import AdaptiveCache
        cache = AdaptiveCache()
        assert cache is not None


class TestIntegrationFeatures:
    """統合機能のテスト"""
    
    @pytest.mark.asyncio
    async def test_multimodal_with_mlops(self):
        """マルチモーダルAI + MLOpsの統合テスト"""
        # マルチモーダル処理
        multimodal_response = client.post(
            "/api/v1/multimodal/process",
            params={"text": "test"}
        )
        assert multimodal_response.status_code == 200
        
        # 量子最適化
        quantum_response = client.post(
            "/api/v3/mlops/quantum-optimize",
            json={
                "locations": [
                    {"latitude": 35.6762, "longitude": 139.6503, "weight": 1.0}
                ],
                "num_select": 1
            }
        )
        assert quantum_response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_adaptive_fusion_with_quantum(self):
        """適応的融合 + 量子最適化の統合テスト"""
        request_data = {
            "modality_results": [
                {
                    "modality": "text",
                    "data": {"text": "test"},
                    "confidence": 0.8,
                    "metadata": {}
                }
            ],
            "locations": [
                {"latitude": 35.6762, "longitude": 139.6503, "weight": 1.0}
            ],
            "strategy": "context_aware"
        }
        
        response = client.post(
            "/api/v3/integrated/quantum-optimized-fusion",
            json=request_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "quantum_optimization" in data or "quantum_optimized" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

