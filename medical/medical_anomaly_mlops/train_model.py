"""
医療データ異常検知MLOps - モデル学習
Isolation Forestによる異常検知モデル
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix
import pickle
from datetime import datetime
import json

print("="*60)
print("医療データ異常検知MLOps - モデル学習")
print("="*60)

# データ読み込み
print("\n📂 データ読み込み中...")
df = pd.read_csv('medical_data_sample.csv')
print(f"✅ データ読み込み完了: {len(df)}件")

# 特徴量抽出
X = df[['channel1', 'channel2', 'channel3']].values
y_true = df['is_anomaly'].values

print(f"\n特徴量: {X.shape}")
print(f"異常データ: {y_true.sum()}件 ({y_true.sum()/len(y_true)*100:.1f}%)")

# モデル学習
print("\n🤖 Isolation Forestモデル学習中...")
model = IsolationForest(
    contamination=0.1,  # 10%が異常と仮定
    random_state=42,
    n_estimators=100
)

model.fit(X)
print("✅ 学習完了")

# 予測
print("\n📊 異常検知実行中...")
predictions = model.predict(X)
# Isolation Forestは-1が異常、1が正常
y_pred = np.where(predictions == -1, 1, 0)

# 評価
print("\n📈 評価結果:")
print(classification_report(y_true, y_pred, target_names=['正常', '異常']))

print("\n混同行列:")
cm = confusion_matrix(y_true, y_pred)
print(cm)

# 精度計算
accuracy = np.sum(y_true == y_pred) / len(y_true)
print(f"\n✅ 精度: {accuracy*100:.2f}%")

# モデル保存
model_file = 'anomaly_detection_model.pkl'
with open(model_file, 'wb') as f:
    pickle.dump(model, f)
print(f"\n💾 モデル保存完了: {model_file}")

# メタデータ保存
metadata = {
    "model_name": "medical_anomaly_detection",
    "version": "1.0",
    "algorithm": "Isolation Forest",
    "accuracy": float(accuracy),
    "contamination": 0.1,
    "n_estimators": 100,
    "trained_at": datetime.now().isoformat(),
    "samples": len(df),
    "features": ["channel1", "channel2", "channel3"]
}

with open('model_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print(f"✅ メタデータ保存完了: model_metadata.json")
print("\n🎉 MLOpsモデル学習完了！")

