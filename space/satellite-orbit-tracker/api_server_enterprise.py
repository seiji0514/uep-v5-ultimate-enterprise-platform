"""
衛星軌道追跡システム - FastAPI REST API（企業レベル）
エラーハンドリング、ロギング、バリデーション強化版

作成日: 2025年11月2日
作成者: 小川清志
"""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional
from datetime import datetime
import time
import traceback

from orbit_calculator import OrbitCalculator, ISSOrbitCalculator
from config import settings
from logger import logger, log_api_request, log_orbit_calculation, log_error

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

# グローバルインスタンス
iss_calculator = ISSOrbitCalculator()
orbit_calculator = OrbitCalculator()


# ==================== ミドルウェア ====================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    全リクエストをログ記録
    """
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
    """
    バリデーションエラーハンドラ
    """
    log_error("Validation Error", str(exc.errors()))
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "detail": exc.errors(),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    HTTPエラーハンドラ
    """
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
    """
    全般的なエラーハンドラ
    """
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

class Position(BaseModel):
    x: float = Field(..., description="X座標 (km)")
    y: float = Field(..., description="Y座標 (km)")
    z: float = Field(..., description="Z座標 (km)")


class Velocity(BaseModel):
    vx: float = Field(..., description="X方向速度 (km/s)")
    vy: float = Field(..., description="Y方向速度 (km/s)")
    vz: float = Field(..., description="Z方向速度 (km/s)")


class Geographic(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="緯度 (degrees)")
    lon: float = Field(..., ge=-180, le=180, description="経度 (degrees)")
    alt: float = Field(..., gt=0, description="高度 (km)")


class SatellitePosition(BaseModel):
    timestamp: str
    satellite: str
    position_eci: Position
    velocity_eci: Velocity
    geographic: Geographic


class OrbitPredictionRequest(BaseModel):
    duration_hours: float = Field(
        default=24.0,
        gt=0,
        le=settings.MAX_PREDICTION_HOURS,
        description="予測期間（時間）"
    )
    step_minutes: float = Field(
        default=5.0,
        gt=0,
        le=60,
        description="計算間隔（分）"
    )
    
    @validator('duration_hours')
    def validate_duration(cls, v):
        if v > settings.MAX_PREDICTION_HOURS:
            raise ValueError(f"予測期間は{settings.MAX_PREDICTION_HOURS}時間以下にしてください")
        return v


class CustomOrbitRequest(BaseModel):
    semi_major_axis: float = Field(..., gt=6371.0, description="軌道長半径 (km)")
    eccentricity: float = Field(..., ge=0, lt=1, description="離心率")
    inclination: float = Field(..., ge=0, le=180, description="軌道傾斜角 (degrees)")
    raan: float = Field(..., ge=0, lt=360, description="昇交点赤経 (degrees)")
    arg_perigee: float = Field(..., ge=0, lt=360, description="近地点引数 (degrees)")
    mean_anomaly: float = Field(..., ge=0, lt=360, description="平均近点角 (degrees)")
    duration_hours: float = Field(default=24.0, gt=0, le=168.0, description="予測期間（時間）")
    
    @validator('semi_major_axis')
    def validate_semi_major_axis(cls, v):
        if v < 6371.0:
            raise ValueError("軌道長半径は地球半径（6371km）以上にしてください")
        if v > 100000.0:
            raise ValueError("軌道長半径は100,000km以下にしてください")
        return v


# ==================== APIエンドポイント ====================

@app.get("/", tags=["General"])
async def root():
    """
    ルートエンドポイント - API情報
    """
    logger.info("Root endpoint accessed")
    
    return {
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "developer": "小川清志",
        "description": settings.API_DESCRIPTION,
        "status": "operational",
        "endpoints": {
            "/iss/current": "ISS現在位置",
            "/iss/predict": "ISS軌道予測",
            "/orbit/calculate": "カスタム軌道計算",
            "/satellites/list": "衛星リスト",
            "/health": "ヘルスチェック",
            "/docs": "API ドキュメント（Swagger UI）",
            "/redoc": "API ドキュメント（ReDoc）"
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/iss/current", tags=["ISS"], response_model=SatellitePosition)
async def get_iss_current_position():
    """
    国際宇宙ステーション（ISS）の現在位置を取得
    
    Returns:
    --------
    - timestamp: 現在時刻（UTC）
    - position_eci: ECI座標系での位置 (km)
    - velocity_eci: ECI座標系での速度 (km/s)
    - geographic: 地理座標（緯度・経度・高度）
    
    Raises:
    -------
    - 500: 内部サーバーエラー
    """
    try:
        logger.info("ISS current position request received")
        start_time = time.time()
        
        position = iss_calculator.get_current_position()
        
        calc_time_ms = (time.time() - start_time) * 1000
        logger.info(f"ISS position calculated in {calc_time_ms:.2f}ms")
        
        return position
    
    except Exception as e:
        log_error("ISS Position Calculation Error", str(e), traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ISS位置計算エラー: {str(e)}"
        )


@app.post("/iss/predict", tags=["ISS"])
async def predict_iss_orbit(request: OrbitPredictionRequest):
    """
    ISSの軌道を予測
    
    Parameters:
    -----------
    - duration_hours: 予測時間（時間）[デフォルト: 24, 最大: 168]
    - step_minutes: 計算間隔（分）[デフォルト: 5, 最大: 60]
    
    Returns:
    --------
    - orbit_data: 軌道データのリスト
    - metadata: メタデータ（計算条件、統計情報）
    
    Raises:
    -------
    - 422: バリデーションエラー
    - 500: 内部サーバーエラー
    """
    try:
        logger.info(f"ISS orbit prediction request: duration={request.duration_hours}h, step={request.step_minutes}min")
        start_time = time.time()
        
        orbit_data = iss_calculator.predict_orbit(
            duration_hours=request.duration_hours
        )
        
        calc_time_ms = (time.time() - start_time) * 1000
        log_orbit_calculation("ISS", request.duration_hours, len(orbit_data), calc_time_ms)
        
        return {
            "satellite": "ISS",
            "prediction_start": orbit_data[0]['timestamp'],
            "prediction_end": orbit_data[-1]['timestamp'],
            "duration_hours": request.duration_hours,
            "data_points": len(orbit_data),
            "orbit_data": orbit_data,
            "metadata": {
                "calculation_method": "Kepler軌道要素",
                "coordinate_system": "ECI (Earth-Centered Inertial)",
                "calculation_time_ms": calc_time_ms,
                "developer": "小川清志",
                "created_at": datetime.utcnow().isoformat()
            }
        }
    
    except ValueError as e:
        log_error("Validation Error", str(e))
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    
    except Exception as e:
        log_error("ISS Orbit Prediction Error", str(e), traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ISS軌道予測エラー: {str(e)}"
        )


@app.post("/orbit/calculate", tags=["Orbit"])
async def calculate_custom_orbit(request: CustomOrbitRequest):
    """
    カスタム軌道要素から軌道を計算
    
    Parameters:
    -----------
    - semi_major_axis: 軌道長半径 (km) [> 6371]
    - eccentricity: 離心率 [0 <= e < 1]
    - inclination: 軌道傾斜角 (degrees) [0-180]
    - raan: 昇交点赤経 (degrees) [0-360]
    - arg_perigee: 近地点引数 (degrees) [0-360]
    - mean_anomaly: 平均近点角 (degrees) [0-360]
    - duration_hours: 予測時間（時間）[デフォルト: 24, 最大: 168]
    
    Returns:
    --------
    - orbital_elements: 入力軌道要素
    - orbit_data: 軌道データのリスト
    - metadata: メタデータ
    
    Raises:
    -------
    - 422: バリデーションエラー
    - 500: 内部サーバーエラー
    """
    try:
        logger.info(f"Custom orbit calculation request: a={request.semi_major_axis}km, e={request.eccentricity}")
        start_time = time.time()
        
        epoch = datetime.utcnow()
        
        orbit_data = orbit_calculator.propagate_orbit(
            semi_major_axis=request.semi_major_axis,
            eccentricity=request.eccentricity,
            inclination=request.inclination,
            raan=request.raan,
            arg_perigee=request.arg_perigee,
            mean_anomaly_0=request.mean_anomaly,
            epoch=epoch,
            duration_hours=request.duration_hours
        )
        
        calc_time_ms = (time.time() - start_time) * 1000
        log_orbit_calculation("Custom", request.duration_hours, len(orbit_data), calc_time_ms)
        
        return {
            "orbital_elements": {
                "semi_major_axis": request.semi_major_axis,
                "eccentricity": request.eccentricity,
                "inclination": request.inclination,
                "raan": request.raan,
                "arg_perigee": request.arg_perigee,
                "mean_anomaly": request.mean_anomaly
            },
            "epoch": epoch.isoformat(),
            "duration_hours": request.duration_hours,
            "data_points": len(orbit_data),
            "orbit_data": orbit_data,
            "metadata": {
                "calculation_time_ms": calc_time_ms,
                "created_at": datetime.utcnow().isoformat()
            }
        }
    
    except ValueError as e:
        log_error("Validation Error", str(e))
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    
    except Exception as e:
        log_error("Custom Orbit Calculation Error", str(e), traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"カスタム軌道計算エラー: {str(e)}"
        )


@app.get("/satellites/list", tags=["Satellites"])
async def list_satellites():
    """
    利用可能な衛星のリスト
    """
    logger.info("Satellite list request received")
    
    return {
        "satellites": [
            {
                "name": "ISS",
                "full_name": "International Space Station",
                "orbit_type": "LEO (Low Earth Orbit)",
                "altitude_km": 420,
                "inclination_deg": 51.6,
                "period_minutes": 92.9,
                "status": "active"
            }
        ],
        "total": 1,
        "note": "現在はISSのみ対応。将来的に他の衛星も追加予定",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health", tags=["General"])
async def health_check():
    """
    ヘルスチェック
    
    Returns:
    --------
    - status: サービスステータス
    - version: APIバージョン
    - uptime: 稼働時間
    - endpoints_available: 利用可能なエンドポイント数
    """
    logger.debug("Health check request received")
    
    return {
        "status": "healthy",
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints_available": 8,
        "log_level": settings.LOG_LEVEL
    }


@app.get("/demo", response_class=HTMLResponse, tags=["General"])
async def demo_page():
    """
    デモページ（HTMLファイルを返す）
    """
    try:
        with open('dashboard.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        logger.info("Demo page served successfully")
        return HTMLResponse(content=html_content)
    
    except FileNotFoundError:
        logger.error("dashboard.html not found")
        return HTMLResponse(
            content="<h1>Dashboard not found</h1><p>dashboard.html が見つかりません</p>",
            status_code=404
        )


# ==================== サーバー起動 ====================

if __name__ == "__main__":
    import uvicorn
    
    logger.info("="*60)
    logger.info("衛星軌道追跡システム - FastAPI REST API（企業レベル）")
    logger.info("="*60)
    logger.info(f"Version: {settings.API_VERSION}")
    logger.info(f"Log Level: {settings.LOG_LEVEL}")
    logger.info("🚀 サーバー起動中...")
    logger.info("")
    logger.info("API エンドポイント:")
    logger.info(f"  - http://{settings.HOST}:{settings.PORT}/")
    logger.info(f"  - http://{settings.HOST}:{settings.PORT}/iss/current")
    logger.info(f"  - http://{settings.HOST}:{settings.PORT}/iss/predict")
    logger.info(f"  - http://{settings.HOST}:{settings.PORT}/docs (Swagger UI)")
    logger.info(f"  - http://{settings.HOST}:{settings.PORT}/demo (3D可視化ダッシュボード)")
    logger.info("")
    logger.info("="*60)
    
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )

