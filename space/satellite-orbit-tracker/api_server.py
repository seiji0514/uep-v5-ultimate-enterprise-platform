"""
衛星軌道追跡システム - FastAPI REST API

作成日: 2025年11月1日
作成者: 小川清志
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import json

from orbit_calculator import OrbitCalculator, ISSOrbitCalculator

app = FastAPI(
    title="Satellite Orbit Tracker API",
    description="衛星軌道計算・追跡システム - 宇宙開発向けAI/MLシステム",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# グローバルインスタンス
iss_calculator = ISSOrbitCalculator()
orbit_calculator = OrbitCalculator()

# Pydanticモデル
class Position(BaseModel):
    x: float
    y: float
    z: float

class Velocity(BaseModel):
    vx: float
    vy: float
    vz: float

class Geographic(BaseModel):
    lat: float
    lon: float
    alt: float

class SatellitePosition(BaseModel):
    timestamp: str
    satellite: str
    position_eci: Position
    velocity_eci: Velocity
    geographic: Geographic

class OrbitPredictionRequest(BaseModel):
    duration_hours: float = 24.0
    step_minutes: float = 5.0

class CustomOrbitRequest(BaseModel):
    semi_major_axis: float
    eccentricity: float
    inclination: float
    raan: float
    arg_perigee: float
    mean_anomaly: float
    duration_hours: float = 24.0


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "service": "Satellite Orbit Tracker API",
        "version": "1.0.0",
        "developer": "小川清志",
        "description": "衛星軌道計算・追跡システム（宇宙開発向けAI/MLシステム）",
        "endpoints": {
            "/iss/current": "ISS現在位置",
            "/iss/predict": "ISS軌道予測",
            "/orbit/calculate": "カスタム軌道計算",
            "/health": "ヘルスチェック",
            "/docs": "API ドキュメント（Swagger UI）"
        }
    }


@app.get("/iss/current")
async def get_iss_current_position():
    """
    国際宇宙ステーション（ISS）の現在位置を取得
    
    Returns:
    --------
    - timestamp: 現在時刻（UTC）
    - position_eci: ECI座標系での位置 (km)
    - velocity_eci: ECI座標系での速度 (km/s)
    - geographic: 地理座標（緯度・経度・高度）
    """
    try:
        position = iss_calculator.get_current_position()
        return position
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/iss/predict")
async def predict_iss_orbit(request: OrbitPredictionRequest):
    """
    ISSの軌道を予測
    
    Parameters:
    -----------
    - duration_hours: 予測時間（時間）
    - step_minutes: 計算間隔（分）
    
    Returns:
    --------
    - orbit_data: 軌道データのリスト
    - metadata: メタデータ（計算条件）
    """
    try:
        orbit_data = iss_calculator.predict_orbit(
            duration_hours=request.duration_hours
        )
        
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
                "developer": "小川清志",
                "created_at": datetime.utcnow().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/orbit/calculate")
async def calculate_custom_orbit(request: CustomOrbitRequest):
    """
    カスタム軌道要素から軌道を計算
    
    Parameters:
    -----------
    - semi_major_axis: 軌道長半径 (km)
    - eccentricity: 離心率
    - inclination: 軌道傾斜角 (degrees)
    - raan: 昇交点赤経 (degrees)
    - arg_perigee: 近地点引数 (degrees)
    - mean_anomaly: 平均近点角 (degrees)
    - duration_hours: 予測時間（時間）
    """
    try:
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
            "orbit_data": orbit_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/satellites/list")
async def list_satellites():
    """利用可能な衛星のリスト"""
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
        "note": "現在はISSのみ対応。将来的に他の衛星も追加予定"
    }


@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {
        "status": "healthy",
        "service": "Satellite Orbit Tracker",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints_available": 6
    }


@app.get("/demo", response_class=HTMLResponse)
async def demo_page():
    """デモページ（HTMLファイルを返す）"""
    try:
        with open('dashboard.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>Dashboard not found</h1><p>dashboard.html が見つかりません</p>",
            status_code=404
        )


if __name__ == "__main__":
    import uvicorn
    print("="*60)
    print("衛星軌道追跡システム - FastAPI REST API")
    print("="*60)
    print("\n🚀 サーバー起動中...")
    print("\nAPI エンドポイント:")
    print("  - http://localhost:8000/")
    print("  - http://localhost:8000/iss/current")
    print("  - http://localhost:8000/iss/predict")
    print("  - http://localhost:8000/docs (Swagger UI)")
    print("  - http://localhost:8000/demo (3D可視化ダッシュボード)")
    print("\n" + "="*60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

