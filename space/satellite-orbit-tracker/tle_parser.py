"""
TLE（Two-Line Element）パーサー
NASA標準フォーマットのTLEデータを解析

作成日: 2025年11月2日
作成者: 小川清志
"""

import re
from dataclasses import dataclass
from typing import Tuple, Optional
from datetime import datetime, timedelta
import math


@dataclass
class TLEData:
    """TLE データクラス"""
    # Line 0 (衛星名)
    name: str
    
    # Line 1
    satellite_number: int
    classification: str
    international_designator: str
    epoch_year: int
    epoch_day: float
    mean_motion_derivative: float
    mean_motion_second_derivative: float
    bstar_drag: float
    ephemeris_type: int
    element_number: int
    
    # Line 2
    inclination: float  # degrees
    raan: float  # Right Ascension of Ascending Node (degrees)
    eccentricity: float
    arg_perigee: float  # Argument of Perigee (degrees)
    mean_anomaly: float  # degrees
    mean_motion: float  # revolutions per day
    revolution_number: int
    
    # 計算済み軌道要素
    epoch: datetime
    semi_major_axis: float  # km
    orbital_period: float  # minutes


class TLEParser:
    """TLEパーサー"""
    
    # 地球の重力定数 (km^3/s^2)
    MU = 398600.4418
    # 地球の平均半径 (km)
    EARTH_RADIUS = 6371.0
    
    def __init__(self):
        self.earth_radius = self.EARTH_RADIUS
        self.mu = self.MU
    
    def parse(self, tle_lines: list) -> TLEData:
        """
        TLE 3行データを解析
        
        Parameters:
        -----------
        tle_lines : list
            [衛星名, Line1, Line2] の3行
            
        Returns:
        --------
        TLEData オブジェクト
        """
        if len(tle_lines) != 3:
            raise ValueError("TLEデータは3行（衛星名、Line1、Line2）が必要です")
        
        name = tle_lines[0].strip()
        line1 = tle_lines[1].strip()
        line2 = tle_lines[2].strip()
        
        # Line1の解析
        satellite_number = int(line1[2:7])
        classification = line1[7]
        international_designator = line1[9:17].strip()
        epoch_year = int(line1[18:20])
        epoch_day = float(line1[20:32])
        mean_motion_derivative = float(line1[33:43])
        mean_motion_second_derivative = self._parse_exponential(line1[44:52])
        bstar_drag = self._parse_exponential(line1[53:61])
        ephemeris_type = int(line1[62])
        element_number = int(line1[64:68])
        
        # Line2の解析
        inclination = float(line2[8:16])
        raan = float(line2[17:25])
        eccentricity = float('0.' + line2[26:33])
        arg_perigee = float(line2[34:42])
        mean_anomaly = float(line2[43:51])
        mean_motion = float(line2[52:63])
        revolution_number = int(line2[63:68])
        
        # エポック時刻を計算
        full_year = 2000 + epoch_year if epoch_year < 57 else 1900 + epoch_year
        epoch = self._epoch_from_day_of_year(full_year, epoch_day)
        
        # 軌道長半径を計算
        # Kepler's third law: n = sqrt(mu / a^3)
        # n = mean_motion (rev/day) * 2*pi / 86400 (rad/s)
        n_rad_per_sec = mean_motion * 2 * math.pi / 86400
        semi_major_axis = (self.mu / (n_rad_per_sec ** 2)) ** (1/3)
        
        # 軌道周期（分）
        orbital_period = 1440 / mean_motion  # 1440 = 24時間 * 60分
        
        return TLEData(
            name=name,
            satellite_number=satellite_number,
            classification=classification,
            international_designator=international_designator,
            epoch_year=epoch_year,
            epoch_day=epoch_day,
            mean_motion_derivative=mean_motion_derivative,
            mean_motion_second_derivative=mean_motion_second_derivative,
            bstar_drag=bstar_drag,
            ephemeris_type=ephemeris_type,
            element_number=element_number,
            inclination=inclination,
            raan=raan,
            eccentricity=eccentricity,
            arg_perigee=arg_perigee,
            mean_anomaly=mean_anomaly,
            mean_motion=mean_motion,
            revolution_number=revolution_number,
            epoch=epoch,
            semi_major_axis=semi_major_axis,
            orbital_period=orbital_period
        )
    
    def _parse_exponential(self, exp_str: str) -> float:
        """
        TLE形式の指数表記を解析
        例: " 12345-3" -> +0.12345e-3
        例: "-12345-3" -> -0.12345e-3
        
        形式: [符号]仮数部(5桁)-指数部(1桁)
        """
        exp_str = exp_str.strip()
        if not exp_str or exp_str == "00000-0" or exp_str == "00000+0":
            return 0.0
        
        # 符号を判定
        if exp_str[0] == '-':
            sign = -1
            exp_str = exp_str[1:]  # 符号を削除
        elif exp_str[0] == '+':
            sign = 1
            exp_str = exp_str[1:]  # 符号を削除
        else:
            sign = 1  # 省略時は+
        
        # 指数部を抽出（最後の-Xまたは+X）
        if '-' in exp_str:
            parts = exp_str.rsplit('-', 1)
            mantissa_str = parts[0]
            exponent = int(parts[1])
        elif '+' in exp_str:
            parts = exp_str.rsplit('+', 1)
            mantissa_str = parts[0]
            exponent = -int(parts[1])  # +の場合は正の指数
        else:
            raise ValueError(f"Invalid exponential format: {exp_str}")
        
        # 仮数部を取得（5桁）
        mantissa = int(mantissa_str)
        
        # 値を計算
        value = sign * (mantissa / 100000.0) * (10 ** (-exponent))
        return value
    
    def _epoch_from_day_of_year(self, year: int, day_of_year: float) -> datetime:
        """
        年と年内通算日から日時を計算
        
        Parameters:
        -----------
        year : int
            年（4桁）
        day_of_year : float
            年内通算日（1.0から始まる）
            
        Returns:
        --------
        datetime オブジェクト
        """
        # 年の始まり
        jan_1 = datetime(year, 1, 1)
        
        # 日数を追加（day_of_year - 1.0 が経過日数）
        delta = timedelta(days=day_of_year - 1.0)
        
        return jan_1 + delta


# ==================== テスト ====================

if __name__ == "__main__":
    print("="*80)
    print("TLEパーサー - テスト")
    print("="*80)
    print()
    
    # ISS の実際のTLEデータ（例）
    iss_tle = [
        "ISS (ZARYA)",
        "1 25544U 98067A   25306.50000000  .00016717  00000-0  10270-3 0  9005",
        "2 25544  51.6400 208.5000 0002500  68.5000 143.6000 15.50030000123456"
    ]
    
    parser = TLEParser()
    
    try:
        tle_data = parser.parse(iss_tle)
        
        print("【TLE解析結果】")
        print(f"衛星名: {tle_data.name}")
        print(f"カタログ番号: {tle_data.satellite_number}")
        print(f"エポック: {tle_data.epoch}")
        print()
        print("【軌道要素】")
        print(f"軌道傾斜角: {tle_data.inclination:.4f}°")
        print(f"昇交点赤経: {tle_data.raan:.4f}°")
        print(f"離心率: {tle_data.eccentricity:.6f}")
        print(f"近地点引数: {tle_data.arg_perigee:.4f}°")
        print(f"平均近点角: {tle_data.mean_anomaly:.4f}°")
        print(f"平均運動: {tle_data.mean_motion:.8f} rev/day")
        print()
        print("【計算済みパラメータ】")
        print(f"軌道長半径: {tle_data.semi_major_axis:.2f} km")
        print(f"軌道周期: {tle_data.orbital_period:.2f} 分")
        print(f"高度: {tle_data.semi_major_axis - parser.EARTH_RADIUS:.2f} km")
        print()
        print("✅ TLE解析成功！")
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()

