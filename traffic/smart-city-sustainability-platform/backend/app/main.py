"""
スマートシティ×サステナビリティ統合プラットフォーム
メインアプリケーションファイル
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from loguru import logger

from app.api import sensors, environment, traffic, energy, esg, dashboard, alerts, decision_support
from app.core.config import settings
from app.core.database import engine, Base
from app.core.influxdb_client import influxdb_client
from app.core.kafka_producer import kafka_producer

# ログ設定
logging.basicConfig(level=logging.INFO)
logger.add("logs/app.log", rotation="10 MB", retention="7 days", level="INFO")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションの起動・終了時の処理"""
    # 起動時
    logger.info("アプリケーション起動中...")
    
    # データベーステーブルの作成
    Base.metadata.create_all(bind=engine)
    logger.info("データベーステーブル作成完了")
    
    # InfluxDB接続確認
    try:
        await influxdb_client.ping()
        logger.info("InfluxDB接続成功")
    except Exception as e:
        logger.error(f"InfluxDB接続エラー: {e}")
    
    # Kafka接続確認
    try:
        kafka_producer.get_metadata()
        logger.info("Kafka接続成功")
    except Exception as e:
        logger.error(f"Kafka接続エラー: {e}")
    
    logger.info("アプリケーション起動完了")
    
    yield
    
    # 終了時
    logger.info("アプリケーション終了中...")
    await influxdb_client.close()
    kafka_producer.close()
    logger.info("アプリケーション終了完了")


# FastAPIアプリケーションの作成
app = FastAPI(
    title="スマートシティ×サステナビリティ統合プラットフォーム",
    description="サステナビリティ・環境管理統合プラットフォームとIoT・スマートシティ統合プラットフォームを統合したシステム",
    version="1.0.0",
    lifespan=lifespan
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(sensors.router, prefix="/api/v1/sensors", tags=["IoTセンサー"])
app.include_router(environment.router, prefix="/api/v1/environment", tags=["環境データ"])
app.include_router(traffic.router, prefix="/api/v1/traffic", tags=["交通データ"])
app.include_router(energy.router, prefix="/api/v1/energy", tags=["エネルギーデータ"])
app.include_router(esg.router, prefix="/api/v1/esg", tags=["ESGレポート"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["ダッシュボード"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["アラート"])
app.include_router(decision_support.router, prefix="/api/v1/decision-support", tags=["判断支援"])


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "スマートシティ×サステナビリティ統合プラットフォーム API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {
        "status": "healthy",
        "service": "smart-city-sustainability-platform"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """グローバル例外ハンドラー"""
    logger.error(f"予期しないエラー: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "内部サーバーエラーが発生しました"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

