"""
TLEデータ取得モジュール
CelestrakからNASA公式TLEデータを取得

作成日: 2025年11月2日
作成者: 小川清志
"""

import requests
from typing import List, Dict, Optional
from datetime import datetime
import json
from pathlib import Path

from tle_parser import TLEParser, TLEData
from logger import logger


class TLEFetcher:
    """Celestrak TLE データ取得クラス"""
    
    # Celestrak TLE データ URL
    BASE_URL = "https://celestrak.org/NORAD/elements/gp.php"
    
    # 主要な衛星グループ
    GROUPS = {
        "stations": "space-stations",  # 宇宙ステーション（ISS含む）
        "active": "active",  # 全アクティブ衛星
        "weather": "weather",  # 気象衛星
        "communications": "communications",  # 通信衛星
        "science": "science",  # 科学衛星
        "navigation": "navigation",  # GPS等
    }
    
    def __init__(self, cache_dir: str = "tle_cache"):
        """
        初期化
        
        Parameters:
        -----------
        cache_dir : str
            TLEキャッシュディレクトリ
        """
        self.parser = TLEParser()
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        logger.info(f"TLEFetcher initialized with cache_dir: {cache_dir}")
    
    def fetch_group(self, group: str, format: str = "3le") -> List[TLEData]:
        """
        衛星グループのTLEデータを取得
        
        Parameters:
        -----------
        group : str
            衛星グループ名（"stations", "active"等）
        format : str
            データ形式（"3le": 3行形式、"json": JSON形式）
            
        Returns:
        --------
        TLEData オブジェクトのリスト
        """
        group_id = self.GROUPS.get(group, group)
        
        params = {
            "GROUP": group_id,
            "FORMAT": format
        }
        
        try:
            logger.info(f"Fetching TLE data for group: {group} ({group_id})")
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            if format == "3le":
                return self._parse_3le_text(response.text)
            elif format == "json":
                return self._parse_json(response.json())
            else:
                raise ValueError(f"Unsupported format: {format}")
        
        except requests.RequestException as e:
            logger.error(f"Failed to fetch TLE data: {e}")
            # キャッシュから読み込みを試みる
            return self._load_from_cache(group)
        
        except Exception as e:
            logger.error(f"Unexpected error in fetch_group: {e}")
            raise
    
    def fetch_satellite(self, satellite_id: int) -> Optional[TLEData]:
        """
        特定の衛星のTLEデータを取得
        
        Parameters:
        -----------
        satellite_id : int
            NORAD カタログ番号（例: ISS = 25544）
            
        Returns:
        --------
        TLEData オブジェクト、または None
        """
        params = {
            "CATNR": satellite_id,
            "FORMAT": "3le"
        }
        
        try:
            logger.info(f"Fetching TLE data for satellite: {satellite_id}")
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            tle_list = self._parse_3le_text(response.text)
            if tle_list:
                return tle_list[0]
            return None
        
        except Exception as e:
            logger.error(f"Failed to fetch satellite {satellite_id}: {e}")
            return None
    
    def _parse_3le_text(self, text: str) -> List[TLEData]:
        """
        3行形式のTLEテキストを解析
        
        Parameters:
        -----------
        text : str
            TLE テキスト（3行ごとに1衛星）
            
        Returns:
        --------
        TLEData オブジェクトのリスト
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        tle_list = []
        
        # 3行ずつ処理
        for i in range(0, len(lines), 3):
            if i + 2 < len(lines):
                try:
                    tle_data = self.parser.parse([lines[i], lines[i+1], lines[i+2]])
                    tle_list.append(tle_data)
                except Exception as e:
                    logger.warning(f"Failed to parse TLE at line {i}: {e}")
        
        logger.info(f"Parsed {len(tle_list)} satellites from 3LE text")
        return tle_list
    
    def _parse_json(self, json_data: list) -> List[TLEData]:
        """
        JSON形式のTLEデータを解析
        （将来の拡張用）
        """
        # TODO: JSON形式のパーサー実装
        raise NotImplementedError("JSON format parser not implemented yet")
    
    def _load_from_cache(self, group: str) -> List[TLEData]:
        """
        キャッシュからTLEデータを読み込み
        
        Parameters:
        -----------
        group : str
            衛星グループ名
            
        Returns:
        --------
        TLEData オブジェクトのリスト
        """
        cache_file = self.cache_dir / f"{group}_tle.json"
        
        if not cache_file.exists():
            logger.warning(f"Cache file not found: {cache_file}")
            return []
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            logger.info(f"Loaded {len(cache_data)} satellites from cache")
            # TODO: JSONからTLEDataへの変換実装
            return []
        
        except Exception as e:
            logger.error(f"Failed to load cache: {e}")
            return []
    
    def save_to_cache(self, group: str, tle_list: List[TLEData]):
        """
        TLEデータをキャッシュに保存
        
        Parameters:
        -----------
        group : str
            衛星グループ名
        tle_list : List[TLEData]
            TLEデータリスト
        """
        cache_file = self.cache_dir / f"{group}_tle.json"
        
        try:
            # TLEDataをdictに変換
            cache_data = []
            for tle in tle_list:
                cache_data.append({
                    "name": tle.name,
                    "satellite_number": tle.satellite_number,
                    "epoch": tle.epoch.isoformat(),
                    "semi_major_axis": tle.semi_major_axis,
                    "eccentricity": tle.eccentricity,
                    "inclination": tle.inclination,
                    "raan": tle.raan,
                    "arg_perigee": tle.arg_perigee,
                    "mean_anomaly": tle.mean_anomaly,
                    "mean_motion": tle.mean_motion,
                    "orbital_period": tle.orbital_period
                })
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(tle_list)} satellites to cache: {cache_file}")
        
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")


# ==================== テスト ====================

if __name__ == "__main__":
    print("="*80)
    print("TLEデータ取得 - テスト")
    print("="*80)
    print()
    
    fetcher = TLEFetcher()
    
    # ISS（NORAD 25544）のTLEデータを取得
    print("【1】ISS TLEデータ取得")
    print("-"*80)
    iss_tle = fetcher.fetch_satellite(25544)
    
    if iss_tle:
        print(f"✅ ISS TLEデータ取得成功！")
        print(f"   衛星名: {iss_tle.name}")
        print(f"   カタログ番号: {iss_tle.satellite_number}")
        print(f"   エポック: {iss_tle.epoch}")
        print(f"   軌道傾斜角: {iss_tle.inclination:.4f}°")
        print(f"   軌道長半径: {iss_tle.semi_major_axis:.2f} km")
        print(f"   軌道周期: {iss_tle.orbital_period:.2f} 分")
        print(f"   高度: {iss_tle.semi_major_axis - fetcher.parser.EARTH_RADIUS:.2f} km")
    else:
        print("❌ ISS TLEデータ取得失敗")
    
    print()
    print("="*80)
    print("🎉 TLEデータ取得テスト完了！")
    print("="*80)

