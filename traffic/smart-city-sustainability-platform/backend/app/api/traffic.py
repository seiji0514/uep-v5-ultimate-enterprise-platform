"""
交通データAPI
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.services.traffic_service import TrafficService
from loguru import logger

router = APIRouter()


@router.get("/data")
async def get_traffic_data(
    sensor_id: str = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """交通データの取得"""
    try:
        service = TrafficService(db)
        data = await service.get_traffic_data(
            sensor_id=sensor_id,
            start_time=start_time,
            end_time=end_time,
            skip=skip,
            limit=limit
        )
        return data
    except Exception as e:
        logger.error(f"交通データ取得エラー: {e}")
        raise HTTPException(status_code=500, detail="交通データの取得に失敗しました")


@router.post("/data")
async def create_traffic_data(
    sensor_id: str,
    vehicle_count: int,
    average_speed: float,
    occupancy: float,
    db: Session = Depends(get_db)
):
    """交通データの作成"""
    try:
        service = TrafficService(db)
        result = await service.create_traffic_data(
            sensor_id=sensor_id,
            vehicle_count=vehicle_count,
            average_speed=average_speed,
            occupancy=occupancy
        )
        return result
    except Exception as e:
        logger.error(f"交通データ作成エラー: {e}")
        raise HTTPException(status_code=500, detail="交通データの作成に失敗しました")


@router.get("/congestion")
async def get_congestion_data(
    location: str = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """渋滞データの取得"""
    try:
        service = TrafficService(db)
        congestion = service.get_congestion_data(
            location=location,
            start_time=start_time,
            end_time=end_time
        )
        return congestion
    except Exception as e:
        logger.error(f"渋滞データ取得エラー: {e}")
        raise HTTPException(status_code=500, detail="渋滞データの取得に失敗しました")

