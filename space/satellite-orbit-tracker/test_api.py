"""
衛星軌道追跡システム - APIテスト
企業レベルのテストコード

作成日: 2025年11月2日
作成者: 小川清志
"""

import pytest
from fastapi.testclient import TestClient
from api_server_enterprise import app
from datetime import datetime

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
        assert data["version"] == "1.0.0"
    
    def test_health_check(self):
        """ヘルスチェックのテスト"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestISSEndpoints:
    """ISSエンドポイントのテスト"""
    
    def test_iss_current_position(self):
        """ISS現在位置取得のテスト"""
        response = client.get("/iss/current")
        assert response.status_code == 200
        data = response.json()
        
        # 必須フィールドの確認
        assert "timestamp" in data
        assert "satellite" in data
        assert data["satellite"] == "ISS"
        assert "position_eci" in data
        assert "velocity_eci" in data
        assert "geographic" in data
        
        # 位置データの検証
        geo = data["geographic"]
        assert -90 <= geo["lat"] <= 90
        assert -180 <= geo["lon"] <= 180
        assert geo["alt"] > 0
    
    def test_iss_predict_orbit_default(self):
        """ISS軌道予測（デフォルト値）のテスト"""
        response = client.post("/iss/predict", json={})
        assert response.status_code == 200
        data = response.json()
        
        assert data["satellite"] == "ISS"
        assert data["duration_hours"] == 24.0
        assert "orbit_data" in data
        assert len(data["orbit_data"]) > 0
        assert "metadata" in data
    
    def test_iss_predict_orbit_custom(self):
        """ISS軌道予測（カスタム値）のテスト"""
        request_data = {
            "duration_hours": 12.0,
            "step_minutes": 10.0
        }
        response = client.post("/iss/predict", json=request_data)
        assert response.status_code == 200
        data = response.json()
        
        assert data["duration_hours"] == 12.0
        assert len(data["orbit_data"]) > 0
    
    def test_iss_predict_orbit_invalid_duration(self):
        """ISS軌道予測（無効な期間）のテスト"""
        request_data = {
            "duration_hours": 200.0  # 最大値（168時間）を超える
        }
        response = client.post("/iss/predict", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_iss_predict_orbit_negative_duration(self):
        """ISS軌道予測（負の期間）のテスト"""
        request_data = {
            "duration_hours": -10.0
        }
        response = client.post("/iss/predict", json=request_data)
        assert response.status_code == 422


class TestCustomOrbitEndpoints:
    """カスタム軌道エンドポイントのテスト"""
    
    def test_custom_orbit_calculation(self):
        """カスタム軌道計算のテスト"""
        request_data = {
            "semi_major_axis": 6791.0,  # ISS相当
            "eccentricity": 0.0003,
            "inclination": 51.6,
            "raan": 0.0,
            "arg_perigee": 0.0,
            "mean_anomaly": 0.0,
            "duration_hours": 24.0
        }
        response = client.post("/orbit/calculate", json=request_data)
        assert response.status_code == 200
        data = response.json()
        
        assert "orbital_elements" in data
        assert "orbit_data" in data
        assert len(data["orbit_data"]) > 0
        assert data["orbital_elements"]["semi_major_axis"] == 6791.0
    
    def test_custom_orbit_invalid_semi_major_axis(self):
        """カスタム軌道計算（無効な軌道長半径）のテスト"""
        request_data = {
            "semi_major_axis": 5000.0,  # 地球半径以下
            "eccentricity": 0.0,
            "inclination": 0.0,
            "raan": 0.0,
            "arg_perigee": 0.0,
            "mean_anomaly": 0.0
        }
        response = client.post("/orbit/calculate", json=request_data)
        assert response.status_code == 422
    
    def test_custom_orbit_invalid_eccentricity(self):
        """カスタム軌道計算（無効な離心率）のテスト"""
        request_data = {
            "semi_major_axis": 7000.0,
            "eccentricity": 1.5,  # >= 1.0
            "inclination": 0.0,
            "raan": 0.0,
            "arg_perigee": 0.0,
            "mean_anomaly": 0.0
        }
        response = client.post("/orbit/calculate", json=request_data)
        assert response.status_code == 422


class TestSatelliteListEndpoint:
    """衛星リストエンドポイントのテスト"""
    
    def test_satellites_list(self):
        """衛星リスト取得のテスト"""
        response = client.get("/satellites/list")
        assert response.status_code == 200
        data = response.json()
        
        assert "satellites" in data
        assert "total" in data
        assert len(data["satellites"]) == data["total"]
        assert data["total"] >= 1


class TestErrorHandling:
    """エラーハンドリングのテスト"""
    
    def test_not_found_endpoint(self):
        """存在しないエンドポイントのテスト"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_invalid_json(self):
        """無効なJSONのテスト"""
        response = client.post(
            "/iss/predict",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422


# ==================== テスト実行 ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

