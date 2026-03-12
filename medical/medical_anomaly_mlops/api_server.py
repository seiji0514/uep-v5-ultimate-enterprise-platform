"""
医療データ異常検知MLOps - APIサーバー
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import numpy as np
import json
from datetime import datetime
from typing import List

app = FastAPI(title="Medical Anomaly Detection MLOps API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# モデル読み込み
try:
    with open('anomaly_detection_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ モデル読み込み完了")
except:
    model = None
    print("⚠️ モデルファイルが見つかりません。先に train_model.py を実行してください。")

# メタデータ読み込み
try:
    with open('model_metadata.json', 'r', encoding='utf-8') as f:
        metadata = json.load(f)
except:
    metadata = {"status": "not trained"}

class MedicalData(BaseModel):
    channel1: float
    channel2: float
    channel3: float

class PredictionResponse(BaseModel):
    is_anomaly: bool
    anomaly_score: float
    timestamp: str
    channels: List[float]

@app.get("/")
async def root():
    return {
        "status": "running",
        "service": "Medical Anomaly Detection MLOps",
        "version": "1.0",
        "model_loaded": model is not None
    }

@app.get("/metadata")
async def get_metadata():
    """モデルメタデータを取得"""
    return metadata

@app.post("/predict", response_model=PredictionResponse)
async def predict(data: MedicalData):
    """異常検知を実行"""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # 特徴量配列に変換
    X = np.array([[data.channel1, data.channel2, data.channel3]])
    
    # 予測
    prediction = model.predict(X)[0]
    anomaly_score = model.score_samples(X)[0]
    
    # -1が異常、1が正常
    is_anomaly = prediction == -1
    
    return PredictionResponse(
        is_anomaly=bool(is_anomaly),
        anomaly_score=float(anomaly_score),
        timestamp=datetime.now().isoformat(),
        channels=[data.channel1, data.channel2, data.channel3]
    )

@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

