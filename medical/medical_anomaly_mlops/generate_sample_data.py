"""
医療データ異常検知MLOps - サンプルデータ生成
擬似的な医療時系列データを生成
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

print("="*60)
print("医療データ異常検知MLOps - サンプルデータ生成")
print("="*60)

# 正常データ生成
np.random.seed(42)
n_samples = 1000

# 時系列データ（脳波を模擬）
timestamps = [datetime.now() - timedelta(seconds=i) for i in range(n_samples)]

# 正常データ: 平均0、標準偏差1のガウス分布
normal_data = np.random.normal(0, 1, n_samples)

# 異常データを10%追加（てんかん発作を模擬）
anomaly_indices = np.random.choice(n_samples, size=int(n_samples * 0.1), replace=False)
for idx in anomaly_indices:
    # 異常: 振幅が大きい（5-10倍）
    normal_data[idx] = np.random.normal(0, 5)

# 複数チャンネル（脳波は複数電極）
channel1 = normal_data
channel2 = normal_data + np.random.normal(0, 0.2, n_samples)
channel3 = normal_data + np.random.normal(0, 0.3, n_samples)

# DataFrame作成
df = pd.DataFrame({
    'timestamp': timestamps,
    'channel1': channel1,
    'channel2': channel2,
    'channel3': channel3,
    'is_anomaly': [1 if i in anomaly_indices else 0 for i in range(n_samples)]
})

# CSV保存
output_file = 'medical_data_sample.csv'
df.to_csv(output_file, index=False)

print(f"\n✅ サンプルデータ生成完了")
print(f"   ファイル: {output_file}")
print(f"   サンプル数: {n_samples}")
print(f"   異常データ: {len(anomaly_indices)}件 ({len(anomaly_indices)/n_samples*100:.1f}%)")
print(f"   チャンネル数: 3")
print("\nデータの先頭5行:")
print(df.head())
print("\n統計情報:")
print(df.describe())

