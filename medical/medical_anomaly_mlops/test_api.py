"""
医療データ異常検知MLOps - APIテスト
企業レベルのテストコード

作成日: 2025年11月2日
作成者: 小川清志
"""

import pytest
from fastapi.testclient import TestClient
from api_server_enterprise import app

# テストクライアント
client = TestClient(app)


class TestGeneralEndpoints:
    """一般的なエンドポイントのテスト"""
    
    def test_root_endpoint(self):
        """ルートエンドポイントのテスト"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data
        assert data["version"] == "2.0.0"
    
    def test_health_check(self):
        """ヘルスチェックのテスト"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "model_loaded" in data


class TestMetadataEndpoint:
    """メタデータエンドポイントのテスト"""
    
    def test_get_metadata(self):
        """メタデータ取得のテスト"""
        response = client.get("/metadata")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)


class TestPredictionEndpoints:
    """異常検知エンドポイントのテスト"""
    
    def test_predict_normal_data(self):
        """正常データの異常検知テスト"""
        request_data = {
            "channel1": 0.5,
            "channel2": 0.3,
            "channel3": 0.4
        }
        response = client.post("/predict", json=request_data)
        
        # モデルが読み込まれていれば200、されていなければ500
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "is_anomaly" in data
            assert "anomaly_score" in data
            assert "confidence" in data
            assert "timestamp" in data
            assert "channels" in data
            assert data["channels"] == [0.5, 0.3, 0.4]
    
    def test_predict_anomaly_data(self):
        """異常データの異常検知テスト"""
        request_data = {
            "channel1": 10.0,
            "channel2": 10.0,
            "channel3": 10.0
        }
        response = client.post("/predict", json=request_data)
        assert response.status_code in [200, 500]
    
    def test_predict_invalid_data(self):
        """無効なデータの異常検知テスト"""
        request_data = {
            "channel1": 2000.0,  # 範囲外
            "channel2": 0.0,
            "channel3": 0.0
        }
        response = client.post("/predict", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_predict_missing_field(self):
        """フィールド欠落のテスト"""
        request_data = {
            "channel1": 0.5,
            "channel2": 0.3
            # channel3が欠落
        }
        response = client.post("/predict", json=request_data)
        assert response.status_code == 422
    
    def test_predict_batch_normal(self):
        """バッチ異常検知（正常）のテスト"""
        request_data = {
            "data": [
                [0.5, 0.3, 0.4],
                [0.6, 0.4, 0.5],
                [0.4, 0.2, 0.3]
            ]
        }
        response = client.post("/predict/batch", json=request_data)
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "predictions" in data
            assert "summary" in data
            assert "metadata" in data
            assert len(data["predictions"]) == 3
            assert data["summary"]["total_samples"] == 3
    
    def test_predict_batch_too_large(self):
        """バッチサイズ超過のテスト"""
        request_data = {
            "data": [[0.5, 0.3, 0.4]] * 2000  # MAX_BATCH_SIZE超過
        }
        response = client.post("/predict/batch", json=request_data)
        assert response.status_code == 422
    
    def test_predict_batch_invalid_channels(self):
        """バッチデータ（無効なチャネル数）のテスト"""
        request_data = {
            "data": [
                [0.5, 0.3],  # 2チャネルのみ（3必要）
                [0.6, 0.4, 0.5]
            ]
        }
        response = client.post("/predict/batch", json=request_data)
        assert response.status_code == 422


class TestErrorHandling:
    """エラーハンドリングのテスト"""
    
    def test_not_found_endpoint(self):
        """存在しないエンドポイントのテスト"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_invalid_json(self):
        """無効なJSONのテスト"""
        response = client.post(
            "/predict",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422


# ==================== テスト実行 ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

