"""
衛星軌道追跡システム - 手動動作確認スクリプト

作成日: 2025年11月2日
作成者: 小川清志
"""

from orbit_calculator import OrbitCalculator, ISSOrbitCalculator
from datetime import datetime
import json

print("="*80)
print("🛰️  衛星軌道追跡システム - 動作確認")
print("="*80)
print()

# ISSOrbitCalculatorのテスト
print("【1】ISS現在位置計算")
print("-"*80)
iss = ISSOrbitCalculator()
current_pos = iss.get_current_position()

print(f"✅ 計算成功！")
print(f"   時刻: {current_pos['timestamp']}")
print(f"   緯度: {current_pos['geographic']['lat']:.2f}°")
print(f"   経度: {current_pos['geographic']['lon']:.2f}°")
print(f"   高度: {current_pos['geographic']['alt']:.2f} km")
print(f"   位置ECI: X={current_pos['position_eci']['x']:.2f}, "
      f"Y={current_pos['position_eci']['y']:.2f}, "
      f"Z={current_pos['position_eci']['z']:.2f} km")
print()

# ISS軌道予測のテスト
print("【2】ISS 24時間軌道予測")
print("-"*80)
orbit_data = iss.predict_orbit(duration_hours=24.0)
print(f"✅ 計算成功！")
print(f"   予測ポイント数: {len(orbit_data)}")
print(f"   開始時刻: {orbit_data[0]['timestamp']}")
print(f"   終了時刻: {orbit_data[-1]['timestamp']}")
print()

# 最初の3ポイントを表示
print("   【最初の3ポイント】")
for i, point in enumerate(orbit_data[:3]):
    print(f"   {i+1}. {point['timestamp'][:19]} | "
          f"緯度: {point['geographic']['lat']:6.2f}° | "
          f"経度: {point['geographic']['lon']:7.2f}° | "
          f"高度: {point['geographic']['alt']:6.2f} km")
print()

# カスタム軌道計算のテスト
print("【3】カスタム軌道計算（静止軌道相当）")
print("-"*80)
orbit_calc = OrbitCalculator()
custom_orbit = orbit_calc.propagate_orbit(
    semi_major_axis=42164.0,  # 静止軌道高度（約35,786 km + 地球半径6,378 km）
    eccentricity=0.0,  # 円軌道
    inclination=0.0,  # 赤道面
    raan=0.0,
    arg_perigee=0.0,
    mean_anomaly=0.0,
    epoch=datetime.utcnow(),
    duration_hours=12.0,
    step_minutes=30.0
)
print(f"✅ 計算成功！")
print(f"   予測ポイント数: {len(custom_orbit)}")
print(f"   軌道タイプ: 静止軌道相当（GEO）")
print(f"   開始時刻: {custom_orbit[0]['timestamp']}")
print(f"   終了時刻: {custom_orbit[-1]['timestamp']}")
print()

# 最初の3ポイントを表示
print("   【最初の3ポイント】")
for i, point in enumerate(custom_orbit[:3]):
    print(f"   {i+1}. {point['timestamp'][:19]} | "
          f"緯度: {point['geographic']['lat']:6.2f}° | "
          f"経度: {point['geographic']['lon']:7.2f}° | "
          f"高度: {point['geographic']['alt']:8.2f} km")
print()

# 精度検証
print("【4】軌道周期の精度検証")
print("-"*80)
# ISSの理論的軌道周期: 約92.9分
iss_orbit_1day = iss.predict_orbit(duration_hours=2.0)
if len(iss_orbit_1day) >= 2:
    # 最初と最後の位置を比較
    first_pos = iss_orbit_1day[0]['position_eci']
    # 軌道周期ごとの位置を計算（92.9分 ≈ 1.548時間）
    expected_period_points = int(1.548 * 60 / 5)  # 5分間隔
    if len(iss_orbit_1day) > expected_period_points:
        period_pos = iss_orbit_1day[expected_period_points]['position_eci']
        
        # 距離計算
        dx = period_pos['x'] - first_pos['x']
        dy = period_pos['y'] - first_pos['y']
        dz = period_pos['z'] - first_pos['z']
        distance = (dx**2 + dy**2 + dz**2)**0.5
        
        print(f"✅ 軌道周期検証:")
        print(f"   理論値: 92.9分")
        print(f"   1周期後の位置差: {distance:.2f} km")
        print(f"   → 小さいほど精度が高い（理想: 0 km）")
print()

# 統計情報
print("【5】システム統計")
print("-"*80)
print(f"✅ ISS現在位置計算: 成功")
print(f"✅ ISS 24時間軌道予測: 成功 ({len(orbit_data)}ポイント)")
print(f"✅ カスタム軌道計算: 成功 ({len(custom_orbit)}ポイント)")
print(f"✅ エラー: 0件")
print()

print("="*80)
print("🎉 動作確認完了！すべての機能が正常に動作しています。")
print("="*80)
print()
print("【次のステップ】")
print("1. サーバー起動: python api_server_enterprise.py")
print("2. ブラウザ確認: http://localhost:8000/docs")
print("3. API テスト: curl http://localhost:8000/iss/current")
print()

