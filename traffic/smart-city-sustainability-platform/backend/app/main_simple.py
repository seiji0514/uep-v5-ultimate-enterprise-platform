"""
スマートシティ×サステナビリティ統合プラットフォーム
簡素化版メインアプリケーションファイル
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.database import engine, Base

# データベーステーブルの作成
@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションの起動・終了時の処理"""
    # 起動時
    Base.metadata.create_all(bind=engine)
    print("データベーステーブル作成完了")
    yield
    # 終了時
    print("アプリケーション終了")

# FastAPIアプリケーションの作成
app = FastAPI(
    title="スマートシティ×サステナビリティ統合プラットフォーム（簡易版）",
    description="最小限の機能のみを実装したシンプルなバージョン",
    version="1.0.0-simple",
    lifespan=lifespan
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 簡易APIエンドポイント
@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "スマートシティ×サステナビリティ統合プラットフォーム API（簡易版）",
        "version": "1.0.0-simple"
    }

@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {"status": "healthy"}

# センサーAPI（簡易版）
@app.get("/api/v1/sensors/")
async def get_sensors():
    """センサー一覧の取得（簡易版）"""
    return {"sensors": []}

@app.post("/api/v1/sensors/")
async def create_sensor(sensor: dict):
    """センサーの作成（簡易版）"""
    return {"message": "センサーを作成しました", "sensor": sensor}

# 環境データAPI（簡易版）
@app.get("/api/v1/environment/data")
async def get_environment_data():
    """環境データの取得（簡易版）"""
    return {"data": []}

@app.post("/api/v1/environment/data")
async def create_environment_data(data: dict):
    """環境データの作成（簡易版）"""
    return {"message": "環境データを作成しました", "data": data}

# ダッシュボードAPI（簡易版）
@app.get("/api/v1/dashboard/overview")
async def get_dashboard_overview():
    """ダッシュボード概要の取得（簡易版）"""
    return {
        "environment": {"data_points": 0},
        "traffic": {"data_points": 0},
        "energy": {"data_points": 0}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

