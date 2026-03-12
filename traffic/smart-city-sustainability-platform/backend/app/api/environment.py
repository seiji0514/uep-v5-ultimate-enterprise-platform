"""
環境データAPI
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.schemas.environment import EnvironmentDataResponse
from app.services.environment_service import EnvironmentService
from loguru import logger

router = APIRouter()


@router.get("/data", response_model=List[EnvironmentDataResponse])
async def get_environment_data(
    sensor_id: str = None,
    data_type: str = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """環境データの取得"""
    try:
        service = EnvironmentService(db)
        data = await service.get_environment_data(
            sensor_id=sensor_id,
            data_type=data_type,
            start_time=start_time,
            end_time=end_time,
            skip=skip,
            limit=limit
        )
        return data
    except Exception as e:
        logger.error(f"環境データ取得エラー: {e}")
        raise HTTPException(status_code=500, detail="環境データの取得に失敗しました")


@router.post("/data")
async def create_environment_data(
    sensor_id: str,
    data_type: str,
    value: float,
    unit: str,
    db: Session = Depends(get_db)
):
    """環境データの作成"""
    try:
        service = EnvironmentService(db)
        result = await service.create_environment_data(
            sensor_id=sensor_id,
            data_type=data_type,
            value=value,
            unit=unit
        )
        return result
    except Exception as e:
        logger.error(f"環境データ作成エラー: {e}")
        raise HTTPException(status_code=500, detail="環境データの作成に失敗しました")


@router.get("/analysis")
async def analyze_environment_data(
    sensor_id: str,
    data_type: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """環境データの分析"""
    try:
        service = EnvironmentService(db)
        analysis = service.analyze_environment_data(
            sensor_id=sensor_id,
            data_type=data_type,
            start_time=start_time,
            end_time=end_time
        )
        return analysis
    except Exception as e:
        logger.error(f"環境データ分析エラー: {e}")
        raise HTTPException(status_code=500, detail="環境データの分析に失敗しました")


@router.get("/predictions")
async def predict_environment_data(
    sensor_id: str,
    data_type: str,
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """環境データの予測"""
    try:
        service = EnvironmentService(db)
        predictions = service.predict_environment_data(
            sensor_id=sensor_id,
            data_type=data_type,
            hours=hours
        )
        return predictions
    except Exception as e:
        logger.error(f"環境データ予測エラー: {e}")
        raise HTTPException(status_code=500, detail="環境データの予測に失敗しました")

