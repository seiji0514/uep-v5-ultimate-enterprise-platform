"""
軌道計算エンジンのテストコード

作成日: 2025年11月2日
作成者: 小川清志
"""

import pytest
import numpy as np
from datetime import datetime
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from orbit_calculator import OrbitCalculator, ISSOrbitCalculator


class TestOrbitCalculator:
    """OrbitCalculatorクラスのテスト"""
    
    @pytest.fixture
    def calculator(self):
        """テスト用の計算機インスタンス"""
        return OrbitCalculator()
    
    def test_initialization(self, calculator):
        """初期化テスト"""
        assert calculator.earth_radius == 6371.0
        assert calculator.mu == 398600.4418
    
    def test_calculate_position_circular_orbit(self, calculator):
        """円軌道の位置計算テスト"""
        # 赤道上の円軌道
        semi_major_axis = 7000.0  # km
        eccentricity = 0.0
        inclination = 0.0
        raan = 0.0
        arg_perigee = 0.0
        true_anomaly = 0.0
        
        x, y, z = calculator.calculate_position(
            semi_major_axis, eccentricity, inclination,
            raan, arg_perigee, true_anomaly
        )
        
        # 位置ベクトルの大きさが軌道長半径に等しい
        r = np.sqrt(x**2 + y**2 + z**2)
        assert np.isclose(r, semi_major_axis, rtol=1e-6)
        
        # z座標はほぼ0（赤道面上）
        assert np.isclose(z, 0.0, atol=1e-6)
    
    def test_calculate_velocity(self, calculator):
        """速度計算テスト"""
        semi_major_axis = 7000.0
        eccentricity = 0.0
        inclination = 0.0
        raan = 0.0
        arg_perigee = 0.0
        true_anomaly = 0.0
        
        vx, vy, vz = calculator.calculate_velocity(
            semi_major_axis, eccentricity, inclination,
            raan, arg_perigee, true_anomaly
        )
        
        # 速度ベクトルの大きさが妥当な範囲
        v = np.sqrt(vx**2 + vy**2 + vz**2)
        expected_v = np.sqrt(calculator.mu / semi_major_axis)
        assert np.isclose(v, expected_v, rtol=1e-2)
    
    def test_eci_to_geographic(self, calculator):
        """ECI→地理座標変換テスト"""
        # 赤道上の点
        x, y, z = 7000.0, 0.0, 0.0
        timestamp = datetime(2025, 11, 1, 12, 0, 0)
        
        lat, lon, alt = calculator.eci_to_geographic(x, y, z, timestamp)
        
        # 緯度はほぼ0（赤道上）
        assert np.isclose(lat, 0.0, atol=5.0)  # 許容誤差5度
        
        # 高度が妥当な範囲
        expected_alt = 7000.0 - calculator.earth_radius
        assert np.isclose(alt, expected_alt, atol=50.0)
    
    def test_solve_kepler(self, calculator):
        """ケプラー方程式の解法テスト"""
        # 円軌道（e=0）
        M = np.pi / 4  # 45度
        e = 0.0
        E = calculator._solve_kepler(M, e)
        assert np.isclose(E, M, rtol=1e-6)
        
        # 楕円軌道（e=0.1）
        M = np.pi / 4
        e = 0.1
        E = calculator._solve_kepler(M, e)
        # M = E - e*sin(E) を満たす
        M_calculated = E - e * np.sin(E)
        assert np.isclose(M, M_calculated, rtol=1e-6)
    
    def test_propagate_orbit(self, calculator):
        """軌道伝播テスト"""
        semi_major_axis = 7000.0
        eccentricity = 0.0
        inclination = 51.6
        raan = 0.0
        arg_perigee = 0.0
        mean_anomaly_0 = 0.0
        epoch = datetime(2025, 11, 1, 0, 0, 0)
        
        orbit_data = calculator.propagate_orbit(
            semi_major_axis, eccentricity, inclination,
            raan, arg_perigee, mean_anomaly_0, epoch,
            duration_hours=2.0, step_minutes=30.0
        )
        
        # データポイント数が正しい
        expected_points = int(2.0 * 60 / 30.0) + 1
        assert len(orbit_data) == expected_points
        
        # 各データポイントが必要なキーを持つ
        for point in orbit_data:
            assert 'timestamp' in point
            assert 'position_eci' in point
            assert 'velocity_eci' in point
            assert 'geographic' in point


class TestISSOrbitCalculator:
    """ISSOrbitCalculatorクラスのテスト"""
    
    @pytest.fixture
    def iss_calculator(self):
        """テスト用のISS計算機インスタンス"""
        return ISSOrbitCalculator()
    
    def test_initialization(self, iss_calculator):
        """初期化テスト"""
        assert iss_calculator.iss_elements['inclination'] == 51.6
        assert iss_calculator.iss_elements['eccentricity'] < 0.01  # ほぼ円軌道
    
    def test_get_current_position(self, iss_calculator):
        """ISS現在位置取得テスト"""
        position = iss_calculator.get_current_position()
        
        # 必要なキーが存在
        assert 'timestamp' in position
        assert 'satellite' in position
        assert 'position_eci' in position
        assert 'velocity_eci' in position
        assert 'geographic' in position
        assert 'orbital_elements' in position
        
        # 衛星名がISS
        assert position['satellite'] == 'ISS'
        
        # 高度が妥当な範囲（400-450km）
        alt = position['geographic']['alt']
        assert 400.0 <= alt <= 450.0
        
        # 緯度が妥当な範囲（-51.6〜51.6度）
        lat = position['geographic']['lat']
        assert -52.0 <= lat <= 52.0
    
    def test_predict_orbit(self, iss_calculator):
        """ISS軌道予測テスト"""
        orbit_data = iss_calculator.predict_orbit(duration_hours=1.0)
        
        # データポイント数が妥当
        assert len(orbit_data) >= 10
        
        # 各データポイントで高度が妥当な範囲
        for point in orbit_data:
            alt = point['geographic']['alt']
            assert 400.0 <= alt <= 450.0
    
    def test_orbit_continuity(self, iss_calculator):
        """軌道の連続性テスト"""
        orbit_data = iss_calculator.predict_orbit(duration_hours=0.5)
        
        # 連続する2点間の距離が妥当
        for i in range(len(orbit_data) - 1):
            pos1 = orbit_data[i]['position_eci']
            pos2 = orbit_data[i + 1]['position_eci']
            
            dx = pos2['x'] - pos1['x']
            dy = pos2['y'] - pos1['y']
            dz = pos2['z'] - pos1['z']
            distance = np.sqrt(dx**2 + dy**2 + dz**2)
            
            # 5分間の移動距離が妥当な範囲（約2000-3000km）
            assert 1000.0 <= distance <= 5000.0


class TestIntegration:
    """統合テスト"""
    
    def test_full_prediction_workflow(self):
        """完全な予測ワークフローのテスト"""
        # ISSの24時間軌道予測
        iss = ISSOrbitCalculator()
        orbit_data = iss.predict_orbit(duration_hours=24.0)
        
        # データが生成されている
        assert len(orbit_data) > 0
        
        # 24時間分のデータポイント数が妥当
        expected_points = int(24.0 * 60 / 5.0) + 1
        assert len(orbit_data) == expected_points
        
        # 最初と最後のタイムスタンプの差が24時間
        from datetime import datetime
        start_time = datetime.fromisoformat(orbit_data[0]['timestamp'])
        end_time = datetime.fromisoformat(orbit_data[-1]['timestamp'])
        duration = (end_time - start_time).total_seconds() / 3600
        assert np.isclose(duration, 24.0, rtol=0.01)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

