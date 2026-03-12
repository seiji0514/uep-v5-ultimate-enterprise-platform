"""
衛星軌道計算エンジン
国際宇宙ステーション（ISS）等の軌道計算・予測

作成日: 2025年11月1日
作成者: 小川清志
"""

import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json

class OrbitCalculator:
    """衛星軌道計算エンジン"""
    
    def __init__(self):
        self.earth_radius = 6371.0  # km
        self.mu = 398600.4418  # km^3/s^2 (地球の重力定数)
        
    def calculate_position(self, 
                          semi_major_axis: float,
                          eccentricity: float,
                          inclination: float,
                          raan: float,  # 昇交点赤経
                          arg_perigee: float,  # 近地点引数
                          true_anomaly: float) -> Tuple[float, float, float]:
        """
        軌道要素から位置を計算（ECI座標系）
        
        Parameters:
        -----------
        semi_major_axis : float
            軌道長半径 (km)
        eccentricity : float
            離心率
        inclination : float
            軌道傾斜角 (degrees)
        raan : float
            昇交点赤経 (degrees)
        arg_perigee : float
            近地点引数 (degrees)
        true_anomaly : float
            真近点角 (degrees)
            
        Returns:
        --------
        (x, y, z) : tuple
            ECI座標系での位置 (km)
        """
        # 度をラジアンに変換
        inc = np.radians(inclination)
        omega = np.radians(raan)
        w = np.radians(arg_perigee)
        nu = np.radians(true_anomaly)
        
        # 軌道面座標系での位置
        r = semi_major_axis * (1 - eccentricity**2) / (1 + eccentricity * np.cos(nu))
        x_orb = r * np.cos(nu)
        y_orb = r * np.sin(nu)
        
        # ECI座標系への変換
        x = (np.cos(omega) * np.cos(w) - np.sin(omega) * np.sin(w) * np.cos(inc)) * x_orb + \
            (-np.cos(omega) * np.sin(w) - np.sin(omega) * np.cos(w) * np.cos(inc)) * y_orb
            
        y = (np.sin(omega) * np.cos(w) + np.cos(omega) * np.sin(w) * np.cos(inc)) * x_orb + \
            (-np.sin(omega) * np.sin(w) + np.cos(omega) * np.cos(w) * np.cos(inc)) * y_orb
            
        z = (np.sin(w) * np.sin(inc)) * x_orb + (np.cos(w) * np.sin(inc)) * y_orb
        
        return (float(x), float(y), float(z))
    
    def calculate_velocity(self,
                          semi_major_axis: float,
                          eccentricity: float,
                          inclination: float,
                          raan: float,
                          arg_perigee: float,
                          true_anomaly: float) -> Tuple[float, float, float]:
        """
        軌道要素から速度を計算（ECI座標系）
        
        Returns:
        --------
        (vx, vy, vz) : tuple
            ECI座標系での速度 (km/s)
        """
        # 度をラジアンに変換
        inc = np.radians(inclination)
        omega = np.radians(raan)
        w = np.radians(arg_perigee)
        nu = np.radians(true_anomaly)
        
        # 軌道面座標系での速度
        p = semi_major_axis * (1 - eccentricity**2)
        r = p / (1 + eccentricity * np.cos(nu))
        h = np.sqrt(self.mu * p)
        
        vx_orb = -self.mu / h * np.sin(nu)
        vy_orb = self.mu / h * (eccentricity + np.cos(nu))
        
        # ECI座標系への変換
        vx = (np.cos(omega) * np.cos(w) - np.sin(omega) * np.sin(w) * np.cos(inc)) * vx_orb + \
             (-np.cos(omega) * np.sin(w) - np.sin(omega) * np.cos(w) * np.cos(inc)) * vy_orb
             
        vy = (np.sin(omega) * np.cos(w) + np.cos(omega) * np.sin(w) * np.cos(inc)) * vx_orb + \
             (-np.sin(omega) * np.sin(w) + np.cos(omega) * np.cos(w) * np.cos(inc)) * vy_orb
             
        vz = (np.sin(w) * np.sin(inc)) * vx_orb + (np.cos(w) * np.sin(inc)) * vy_orb
        
        return (float(vx), float(vy), float(vz))
    
    def eci_to_geographic(self, x: float, y: float, z: float, 
                         timestamp: datetime) -> Tuple[float, float, float]:
        """
        ECI座標から地理座標（緯度・経度・高度）に変換
        
        Parameters:
        -----------
        x, y, z : float
            ECI座標 (km)
        timestamp : datetime
            時刻（UTC）
            
        Returns:
        --------
        (lat, lon, alt) : tuple
            緯度 (degrees), 経度 (degrees), 高度 (km)
        """
        # 簡易的なGMST計算（地球自転角）
        jd = self._julian_date(timestamp)
        gmst = self._greenwich_mean_sidereal_time(jd)
        
        # ECEF座標への変換
        x_ecef = x * np.cos(gmst) + y * np.sin(gmst)
        y_ecef = -x * np.sin(gmst) + y * np.cos(gmst)
        z_ecef = z
        
        # 地理座標への変換
        lon = np.degrees(np.arctan2(y_ecef, x_ecef))
        r = np.sqrt(x_ecef**2 + y_ecef**2 + z_ecef**2)
        lat = np.degrees(np.arcsin(z_ecef / r))
        alt = r - self.earth_radius
        
        return (float(lat), float(lon), float(alt))
    
    def _julian_date(self, dt: datetime) -> float:
        """ユリウス日を計算"""
        a = (14 - dt.month) // 12
        y = dt.year + 4800 - a
        m = dt.month + 12 * a - 3
        
        jdn = dt.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
        jd = jdn + (dt.hour - 12) / 24 + dt.minute / 1440 + dt.second / 86400
        
        return jd
    
    def _greenwich_mean_sidereal_time(self, jd: float) -> float:
        """グリニッジ平均恒星時（GMST）を計算（ラジアン）"""
        t = (jd - 2451545.0) / 36525.0
        gmst_deg = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + \
                   0.000387933 * t**2 - t**3 / 38710000.0
        gmst_deg = gmst_deg % 360.0
        return np.radians(gmst_deg)
    
    def propagate_orbit(self,
                       semi_major_axis: float,
                       eccentricity: float,
                       inclination: float,
                       raan: float,
                       arg_perigee: float,
                       mean_anomaly_0: float,
                       epoch: datetime,
                       duration_hours: float = 24.0,
                       step_minutes: float = 5.0) -> List[Dict]:
        """
        軌道を時間発展させる
        
        Parameters:
        -----------
        mean_anomaly_0 : float
            エポック時の平均近点角 (degrees)
        epoch : datetime
            エポック時刻
        duration_hours : float
            予測時間 (hours)
        step_minutes : float
            計算間隔 (minutes)
            
        Returns:
        --------
        orbit_data : List[Dict]
            時刻ごとの位置・速度データ
        """
        # 平均運動（rad/s）
        n = np.sqrt(self.mu / semi_major_axis**3)
        
        orbit_data = []
        num_steps = int(duration_hours * 60 / step_minutes)
        
        for i in range(num_steps + 1):
            dt = timedelta(minutes=i * step_minutes)
            current_time = epoch + dt
            
            # 平均近点角の更新
            delta_t = dt.total_seconds()
            mean_anomaly = (np.radians(mean_anomaly_0) + n * delta_t) % (2 * np.pi)
            
            # 離心近点角を解く（ニュートン法）
            E = self._solve_kepler(mean_anomaly, eccentricity)
            
            # 真近点角を計算
            true_anomaly = 2 * np.arctan2(
                np.sqrt(1 + eccentricity) * np.sin(E / 2),
                np.sqrt(1 - eccentricity) * np.cos(E / 2)
            )
            true_anomaly_deg = np.degrees(true_anomaly)
            
            # 位置・速度を計算
            pos = self.calculate_position(
                semi_major_axis, eccentricity, inclination,
                raan, arg_perigee, true_anomaly_deg
            )
            
            vel = self.calculate_velocity(
                semi_major_axis, eccentricity, inclination,
                raan, arg_perigee, true_anomaly_deg
            )
            
            # 地理座標に変換
            lat, lon, alt = self.eci_to_geographic(pos[0], pos[1], pos[2], current_time)
            
            orbit_data.append({
                'timestamp': current_time.isoformat(),
                'position_eci': {'x': pos[0], 'y': pos[1], 'z': pos[2]},
                'velocity_eci': {'vx': vel[0], 'vy': vel[1], 'vz': vel[2]},
                'geographic': {'lat': lat, 'lon': lon, 'alt': alt}
            })
        
        return orbit_data
    
    def _solve_kepler(self, M: float, e: float, tol: float = 1e-8, max_iter: int = 100) -> float:
        """
        ケプラー方程式を解く（ニュートン法）
        M = E - e*sin(E)
        
        Parameters:
        -----------
        M : float
            平均近点角 (radians)
        e : float
            離心率
            
        Returns:
        --------
        E : float
            離心近点角 (radians)
        """
        E = M  # 初期値
        
        for _ in range(max_iter):
            f = E - e * np.sin(E) - M
            f_prime = 1 - e * np.cos(E)
            E_new = E - f / f_prime
            
            if abs(E_new - E) < tol:
                return E_new
            
            E = E_new
        
        return E


class ISSOrbitCalculator:
    """国際宇宙ステーション（ISS）専用の軌道計算"""
    
    def __init__(self):
        self.calculator = OrbitCalculator()
        # ISS標準軌道要素（近似値）
        self.iss_elements = {
            'semi_major_axis': 6371.0 + 420.0,  # 地球半径 + 高度420km
            'eccentricity': 0.0003,  # ほぼ円軌道
            'inclination': 51.6,  # degrees
            'raan': 0.0,  # 昇交点赤経（時刻により変動）
            'arg_perigee': 0.0,  # 近地点引数
            'mean_anomaly': 0.0  # 平均近点角（時刻により変動）
        }
        
    def get_current_position(self) -> Dict:
        """ISSの現在位置を取得"""
        current_time = datetime.utcnow()
        
        # 現在時刻での平均近点角を計算（簡易版）
        # ISS軌道周期: 約92.9分
        epoch = datetime(2025, 11, 1, 0, 0, 0)
        delta_t = (current_time - epoch).total_seconds()
        orbital_period = 92.9 * 60  # seconds
        mean_anomaly = (delta_t / orbital_period * 360) % 360
        
        # 昇交点赤経の計算（簡易版）
        raan = (delta_t / (86400.0) * 360 * 0.9856) % 360  # 地球の歳差運動
        
        pos = self.calculator.calculate_position(
            self.iss_elements['semi_major_axis'],
            self.iss_elements['eccentricity'],
            self.iss_elements['inclination'],
            raan,
            self.iss_elements['arg_perigee'],
            mean_anomaly
        )
        
        vel = self.calculator.calculate_velocity(
            self.iss_elements['semi_major_axis'],
            self.iss_elements['eccentricity'],
            self.iss_elements['inclination'],
            raan,
            self.iss_elements['arg_perigee'],
            mean_anomaly
        )
        
        lat, lon, alt = self.calculator.eci_to_geographic(
            pos[0], pos[1], pos[2], current_time
        )
        
        return {
            'timestamp': current_time.isoformat(),
            'satellite': 'ISS',
            'position_eci': {'x': pos[0], 'y': pos[1], 'z': pos[2]},
            'velocity_eci': {'vx': vel[0], 'vy': vel[1], 'vz': vel[2]},
            'geographic': {'lat': lat, 'lon': lon, 'alt': alt},
            'orbital_elements': {
                'semi_major_axis': self.iss_elements['semi_major_axis'],
                'eccentricity': self.iss_elements['eccentricity'],
                'inclination': self.iss_elements['inclination'],
                'raan': raan,
                'mean_anomaly': mean_anomaly
            }
        }
    
    def predict_orbit(self, duration_hours: float = 24.0) -> List[Dict]:
        """ISS軌道を予測"""
        current_time = datetime.utcnow()
        
        # 現在の軌道要素
        epoch = datetime(2025, 11, 1, 0, 0, 0)
        delta_t = (current_time - epoch).total_seconds()
        orbital_period = 92.9 * 60
        mean_anomaly = (delta_t / orbital_period * 360) % 360
        raan = (delta_t / (86400.0) * 360 * 0.9856) % 360
        
        return self.calculator.propagate_orbit(
            self.iss_elements['semi_major_axis'],
            self.iss_elements['eccentricity'],
            self.iss_elements['inclination'],
            raan,
            self.iss_elements['arg_perigee'],
            mean_anomaly,
            current_time,
            duration_hours=duration_hours,
            step_minutes=5.0
        )


if __name__ == "__main__":
    print("="*60)
    print("衛星軌道計算エンジン - テスト")
    print("="*60)
    
    # ISS軌道計算
    iss = ISSOrbitCalculator()
    
    print("\n【ISS現在位置】")
    current_pos = iss.get_current_position()
    print(f"時刻: {current_pos['timestamp']}")
    print(f"緯度: {current_pos['geographic']['lat']:.2f}°")
    print(f"経度: {current_pos['geographic']['lon']:.2f}°")
    print(f"高度: {current_pos['geographic']['alt']:.2f} km")
    
    print("\n【24時間軌道予測】")
    orbit = iss.predict_orbit(duration_hours=24.0)
    print(f"予測ポイント数: {len(orbit)}")
    print(f"開始時刻: {orbit[0]['timestamp']}")
    print(f"終了時刻: {orbit[-1]['timestamp']}")
    
    # 軌道データをJSON出力
    with open('sample_data/iss_orbit_24h.json', 'w') as f:
        json.dump(orbit, f, indent=2)
    
    print("\n✅ 軌道データを 'sample_data/iss_orbit_24h.json' に保存しました")
    print("\n🎉 軌道計算エンジン テスト完了！")

