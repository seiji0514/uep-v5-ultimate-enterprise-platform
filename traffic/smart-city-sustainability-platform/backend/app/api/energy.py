"""
エネルギーデータAPI
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.services.energy_service import EnergyService
from loguru import logger

router = APIRouter()


@router.get("/data")
async def get_energy_data(
    sensor_id: str = None,
    energy_type: str = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """エネルギーデータの取得"""
    try:
        service = EnergyService(db)
        data = service.get_energy_data(
            sensor_id=sensor_id,
            energy_type=energy_type,
            start_time=start_time,
            end_time=end_time,
            skip=skip,
            limit=limit
        )
        return data
    except Exception as e:
        logger.error(f"エネルギーデータ取得エラー: {e}")
        raise HTTPException(status_code=500, detail="エネルギーデータの取得に失敗しました")


@router.post("/data")
async def create_energy_data(
    sensor_id: str,
    energy_type: str,
    consumption: float,
    generation: float = None,
    db: Session = Depends(get_db)
):
    """エネルギーデータの作成"""
    try:
        service = EnergyService(db)
        result = await service.create_energy_data(
            sensor_id=sensor_id,
            energy_type=energy_type,
            consumption=consumption,
            generation=generation
        )
        return result
    except Exception as e:
        logger.error(f"エネルギーデータ作成エラー: {e}")
        raise HTTPException(status_code=500, detail="エネルギーデータの作成に失敗しました")


@router.get("/balance")
async def get_energy_balance(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """エネルギーバランスの取得"""
    try:
        service = EnergyService(db)
        balance = service.get_energy_balance(
            start_time=start_time,
            end_time=end_time
        )
        return balance
    except Exception as e:
        logger.error(f"エネルギーバランス取得エラー: {e}")
        raise HTTPException(status_code=500, detail="エネルギーバランスの取得に失敗しました")

