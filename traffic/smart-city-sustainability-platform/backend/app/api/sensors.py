"""
IoTセンサーAPI
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.sensor import SensorCreate, SensorResponse
from app.services.sensor_service import SensorService
from loguru import logger

router = APIRouter()


@router.get("/", response_model=List[SensorResponse])
async def get_sensors(
    sensor_type: str = None,
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """IoTセンサー一覧の取得"""
    try:
        service = SensorService(db)
        sensors = service.get_sensors(sensor_type=sensor_type, status=status, skip=skip, limit=limit)
        return sensors
    except Exception as e:
        logger.error(f"センサー一覧取得エラー: {e}")
        raise HTTPException(status_code=500, detail="センサー一覧の取得に失敗しました")


@router.get("/{sensor_id}", response_model=SensorResponse)
async def get_sensor(sensor_id: str, db: Session = Depends(get_db)):
    """IoTセンサー詳細の取得"""
    try:
        service = SensorService(db)
        sensor = service.get_sensor(sensor_id)
        if not sensor:
            raise HTTPException(status_code=404, detail="センサーが見つかりません")
        return sensor
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"センサー詳細取得エラー: {e}")
        raise HTTPException(status_code=500, detail="センサー詳細の取得に失敗しました")


@router.post("/", response_model=SensorResponse)
async def create_sensor(sensor: SensorCreate, db: Session = Depends(get_db)):
    """IoTセンサーの作成"""
    try:
        service = SensorService(db)
        new_sensor = service.create_sensor(sensor)
        return new_sensor
    except Exception as e:
        logger.error(f"センサー作成エラー: {e}")
        raise HTTPException(status_code=500, detail="センサーの作成に失敗しました")


@router.put("/{sensor_id}", response_model=SensorResponse)
async def update_sensor(sensor_id: str, sensor: SensorCreate, db: Session = Depends(get_db)):
    """IoTセンサーの更新"""
    try:
        service = SensorService(db)
        updated_sensor = service.update_sensor(sensor_id, sensor)
        if not updated_sensor:
            raise HTTPException(status_code=404, detail="センサーが見つかりません")
        return updated_sensor
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"センサー更新エラー: {e}")
        raise HTTPException(status_code=500, detail="センサーの更新に失敗しました")


@router.delete("/{sensor_id}")
async def delete_sensor(sensor_id: str, db: Session = Depends(get_db)):
    """IoTセンサーの削除"""
    try:
        service = SensorService(db)
        result = service.delete_sensor(sensor_id)
        if not result:
            raise HTTPException(status_code=404, detail="センサーが見つかりません")
        return {"message": "センサーを削除しました"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"センサー削除エラー: {e}")
        raise HTTPException(status_code=500, detail="センサーの削除に失敗しました")

