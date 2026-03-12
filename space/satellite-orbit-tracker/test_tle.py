"""
TLE統合機能のテスト
企業レベルのNASA TLEデータ統合検証

作成日: 2025年11月2日
作成者: 小川清志
"""

import pytest
from tle_parser import TLEParser, TLEData
from tle_fetcher import TLEFetcher


class TestTLEParser:
    """TLEパーサーのテスト"""
    
    def test_iss_tle_parsing(self):
        """ISS TLE解析のテスト"""
        # ISS の実際のTLEデータ（サンプル）
        iss_tle = [
            "ISS (ZARYA)",
            "1 25544U 98067A   25306.50000000  .00016717  00000-0  10270-3 0  9005",
            "2 25544  51.6400 208.5000 0002500  68.5000 143.6000 15.50030000123456"
        ]
        
        parser = TLEParser()
        tle_data = parser.parse(iss_tle)
        
        # 基本データの検証
        assert tle_data.name == "ISS (ZARYA)"
        assert tle_data.satellite_number == 25544
        assert tle_data.inclination == pytest.approx(51.6400, rel=1e-4)
        assert tle_data.eccentricity == pytest.approx(0.0002500, rel=1e-4)
        assert tle_data.mean_motion == pytest.approx(15.50030000, rel=1e-4)
        
        # 軌道長半径の妥当性チェック（ISSは約6791km）
        assert 6700 < tle_data.semi_major_axis < 6900
        
        # 軌道周期の妥当性チェック（ISSは約92.9分）
        assert 90 < tle_data.orbital_period < 95
    
    def test_tle_parser_validation(self):
        """TLEパーサーのバリデーションテスト"""
        parser = TLEParser()
        
        # 不正な行数
        with pytest.raises(ValueError):
            parser.parse(["Line1", "Line2"])  # 3行必要
    
    def test_exponential_parsing(self):
        """指数表記解析のテスト"""
        parser = TLEParser()
        
        # 正常ケース
        assert parser._parse_exponential(" 12345-3") == pytest.approx(0.00012345)
        assert parser._parse_exponential("-12345-3") == pytest.approx(-0.00012345)
        assert parser._parse_exponential("00000-0") == 0.0


class TestTLEFetcher:
    """TLEフェッチャーのテスト"""
    
    @pytest.mark.skip(reason="オンライン接続が必要")
    def test_fetch_iss(self):
        """ISS TLEデータ取得のテスト（オンライン）"""
        fetcher = TLEFetcher()
        iss_tle = fetcher.fetch_satellite(25544)
        
        assert iss_tle is not None
        assert iss_tle.satellite_number == 25544
        assert "ISS" in iss_tle.name.upper()
    
    @pytest.mark.skip(reason="オンライン接続が必要")
    def test_fetch_stations_group(self):
        """宇宙ステーショングループ取得のテスト（オンライン）"""
        fetcher = TLEFetcher()
        stations = fetcher.fetch_group("stations")
        
        assert len(stations) > 0
        # ISSが含まれているはず
        iss_found = any(25544 == tle.satellite_number for tle in stations)
        assert iss_found


# ==================== テスト実行 ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

