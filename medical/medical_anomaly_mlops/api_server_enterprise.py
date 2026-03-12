"""
医療データ異常検知MLOps - FastAPI REST API（企業レベル）
エラーハンドリング、ロギング、バリデーション強化版

作成日: 2025年11月2日
作成者: 小川清志
"""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, validator
import pickle
import numpy as np
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
import time
import traceback

from config import settings
from logger import logger, log_api_request, log_prediction, log_error

# FastAPIアプリケーション
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# モデル読み込み
try:
    with open(settings.MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    logger.info(f"✅ モデル読み込み完了: {settings.MODEL_PATH}")
except Exception as e:
    model = None
    logger.warning(f"⚠️ モデルファイルが見つかりません: {str(e)}")

# スケーラー読み込み
try:
    with open(settings.SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    logger.info(f"✅ スケーラー読み込み完了: {settings.SCALER_PATH}")
except Exception as e:
    scaler = None
    logger.warning(f"⚠️ スケーラーファイルが見つかりません: {str(e)}")

# メタデータ読み込み
try:
    with open(settings.METADATA_PATH, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    logger.info(f"✅ メタデータ読み込み完了: {settings.METADATA_PATH}")
except Exception as e:
    metadata = {"status": "not trained", "error": str(e)}
    logger.warning(f"⚠️ メタデータファイルが見つかりません: {str(e)}")


# ==================== ミドルウェア ====================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """全リクエストをログ記録"""
    start_time = time.time()
    
    try:
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000
        
        log_api_request(
            endpoint=str(request.url.path),
            method=request.method,
            status_code=response.status_code,
            duration_ms=duration_ms
        )
        
        return response
    
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        log_error("Middleware Exception", str(e), traceback.format_exc())
        raise


# ==================== 例外ハンドラ ====================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """バリデーションエラーハンドラ"""
    error_details = []
    for error in exc.errors():
        error_dict = {
            "type": error.get("type"),
            "loc": error.get("loc"),
            "msg": error.get("msg"),
            "input": str(error.get("input"))
        }
        error_details.append(error_dict)
    
    log_error("Validation Error", str(error_details))
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "detail": error_details,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTPエラーハンドラ"""
    log_error("HTTP Exception", f"{exc.status_code}: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """全般的なエラーハンドラ"""
    log_error("Unhandled Exception", str(exc), traceback.format_exc())
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# ==================== Pydanticモデル ====================

class MedicalData(BaseModel):
    channel1: float = Field(..., description="チャネル1データ")
    channel2: float = Field(..., description="チャネル2データ")
    channel3: float = Field(..., description="チャネル3データ")
    
    @validator('channel1', 'channel2', 'channel3')
    def validate_channel_data(cls, v):
        if not -1000 <= v <= 1000:
            raise ValueError("チャネルデータは-1000から1000の範囲にしてください")
        return v


class BatchMedicalData(BaseModel):
    data: List[List[float]] = Field(..., description="バッチデータ（複数サンプル）")
    
    @validator('data')
    def validate_batch_data(cls, v):
        if len(v) > settings.MAX_BATCH_SIZE:
            raise ValueError(f"バッチサイズは{settings.MAX_BATCH_SIZE}以下にしてください")
        for sample in v:
            if len(sample) != 3:
                raise ValueError("各サンプルは3チャネルのデータが必要です")
        return v


class PredictionResponse(BaseModel):
    is_anomaly: bool
    anomaly_score: float
    confidence: float
    timestamp: str
    channels: List[float]


class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResponse]
    summary: Dict[str, int]
    metadata: Dict[str, Any]


# ==================== APIエンドポイント ====================

@app.get("/", tags=["General"])
async def root():
    """ルートエンドポイント - API情報"""
    logger.info("Root endpoint accessed")
    
    return {
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "developer": "小川清志",
        "description": settings.API_DESCRIPTION,
        "status": "operational",
        "model_loaded": model is not None,
        "endpoints": {
            "/predict": "異常検知（単一サンプル）",
            "/predict/batch": "異常検知（バッチ処理）",
            "/metadata": "モデルメタデータ",
            "/health": "ヘルスチェック",
            "/docs": "API ドキュメント（Swagger UI）",
            "/redoc": "API ドキュメント（ReDoc）"
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/predict", tags=["Prediction"], response_model=PredictionResponse)
async def predict(data: MedicalData):
    """
    医療データの異常検知を実行（単一サンプル）
    
    Parameters:
    -----------
    - channel1, channel2, channel3: 医療データ（3チャネル）
    
    Returns:
    --------
    - is_anomaly: 異常かどうか（True/False）
    - anomaly_score: 異常スコア
    - confidence: 信頼度
    - timestamp: 予測時刻
    - channels: 入力データ
    
    Raises:
    -------
    - 422: バリデーションエラー
    - 500: モデル未ロード、または内部エラー
    """
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="モデルが読み込まれていません。train_model.py を実行してください。"
        )
    
    try:
        logger.info(f"Prediction request: channels=[{data.channel1}, {data.channel2}, {data.channel3}]")
        start_time = time.time()
        
        # 特徴量配列に変換
        X = np.array([[data.channel1, data.channel2, data.channel3]])
        
        # スケーリング
        if scaler is not None:
            X = scaler.transform(X)
        
        # 予測
        prediction = model.predict(X)[0]
        anomaly_score = model.score_samples(X)[0]
        
        # -1が異常、1が正常
        is_anomaly = prediction == -1
        
        # 信頼度計算（異常スコアの絶対値）
        confidence = min(abs(anomaly_score), 1.0)
        
        calc_time_ms = (time.time() - start_time) * 1000
        log_prediction(1, int(is_anomaly), calc_time_ms, confidence)
        
        return PredictionResponse(
            is_anomaly=bool(is_anomaly),
            anomaly_score=float(anomaly_score),
            confidence=float(confidence),
            timestamp=datetime.utcnow().isoformat(),
            channels=[data.channel1, data.channel2, data.channel3]
        )
    
    except Exception as e:
        log_error("Prediction Error", str(e), traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"異常検知エラー: {str(e)}"
        )


@app.post("/predict/batch", tags=["Prediction"], response_model=BatchPredictionResponse)
async def predict_batch(data: BatchMedicalData):
    """
    医療データの異常検知を実行（バッチ処理）
    
    Parameters:
    -----------
    - data: 複数サンプルのデータ
    
    Returns:
    --------
    - predictions: 各サンプルの予測結果
    - summary: 正常/異常の集計
    - metadata: 処理情報
    """
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="モデルが読み込まれていません"
        )
    
    try:
        logger.info(f"Batch prediction request: {len(data.data)} samples")
        start_time = time.time()
        
        # 配列に変換
        X = np.array(data.data)
        
        # スケーリング
        if scaler is not None:
            X = scaler.transform(X)
        
        # 予測
        predictions_raw = model.predict(X)
        anomaly_scores = model.score_samples(X)
        
        # 結果を整形
        predictions = []
        num_anomalies = 0
        
        for i, (pred, score, original) in enumerate(zip(predictions_raw, anomaly_scores, data.data)):
            is_anomaly = pred == -1
            if is_anomaly:
                num_anomalies += 1
            
            confidence = min(abs(score), 1.0)
            
            predictions.append(PredictionResponse(
                is_anomaly=bool(is_anomaly),
                anomaly_score=float(score),
                confidence=float(confidence),
                timestamp=datetime.utcnow().isoformat(),
                channels=original
            ))
        
        calc_time_ms = (time.time() - start_time) * 1000
        accuracy = metadata.get('accuracy', 0.0) if isinstance(metadata, dict) else 0.0
        log_prediction(len(data.data), num_anomalies, calc_time_ms, accuracy)
        
        return BatchPredictionResponse(
            predictions=predictions,
            summary={
                "total_samples": len(data.data),
                "anomalies": num_anomalies,
                "normal": len(data.data) - num_anomalies
            },
            metadata={
                "processing_time_ms": calc_time_ms,
                "samples_per_second": len(data.data) / (calc_time_ms / 1000),
                "created_at": datetime.utcnow().isoformat()
            }
        )
    
    except Exception as e:
        log_error("Batch Prediction Error", str(e), traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"バッチ異常検知エラー: {str(e)}"
        )


@app.get("/metadata", tags=["Model"])
async def get_metadata():
    """
    モデルメタデータを取得
    
    Returns:
    --------
    モデルの訓練情報、精度、パラメータ等
    """
    logger.info("Metadata request received")
    return metadata


@app.get("/health", tags=["General"])
async def health_check():
    """
    ヘルスチェック
    
    Returns:
    --------
    - status: サービスステータス
    - model_loaded: モデル読み込み状態
    - version: APIバージョン
    - timestamp: 現在時刻
    """
    logger.debug("Health check request received")
    
    return {
        "status": "healthy",
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "timestamp": datetime.utcnow().isoformat(),
        "log_level": settings.LOG_LEVEL
    }


# ==================== サーバー起動 ====================

if __name__ == "__main__":
    import uvicorn
    
    logger.info("="*60)
    logger.info("医療データ異常検知MLOps - FastAPI REST API（企業レベル）")
    logger.info("="*60)
    logger.info(f"Version: {settings.API_VERSION}")
    logger.info(f"Log Level: {settings.LOG_LEVEL}")
    logger.info(f"Model: {settings.MODEL_PATH} ({'Loaded' if model else 'Not Loaded'})")
    logger.info(f"Scaler: {settings.SCALER_PATH} ({'Loaded' if scaler else 'Not Loaded'})")
    logger.info("🚀 サーバー起動中...")
    logger.info("")
    logger.info("API エンドポイント:")
    logger.info(f"  - http://{settings.HOST}:{settings.PORT}/")
    logger.info(f"  - http://{settings.HOST}:{settings.PORT}/predict")
    logger.info(f"  - http://{settings.HOST}:{settings.PORT}/predict/batch")
    logger.info(f"  - http://{settings.HOST}:{settings.PORT}/docs (Swagger UI)")
    logger.info("")
    logger.info("="*60)
    
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )

