"""
アラートAPI
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.alert_service import AlertService
from loguru import logger

router = APIRouter()


@router.get("/")
async def get_alerts(
    sensor_id: str = None,
    alert_type: str = None,
    severity: str = None,
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """アラート一覧の取得"""
    try:
        service = AlertService(db)
        alerts = service.get_alerts(
            sensor_id=sensor_id,
            alert_type=alert_type,
            severity=severity,
            status=status,
            skip=skip,
            limit=limit
        )
        return alerts
    except Exception as e:
        logger.error(f"アラート一覧取得エラー: {e}")
        raise HTTPException(status_code=500, detail="アラート一覧の取得に失敗しました")


@router.post("/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: str,
    user_id: str,
    db: Session = Depends(get_db)
):
    """アラートの承認"""
    try:
        service = AlertService(db)
        result = service.acknowledge_alert(alert_id, user_id)
        if not result:
            raise HTTPException(status_code=404, detail="アラートが見つかりません")
        return {"message": "アラートを承認しました"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"アラート承認エラー: {e}")
        raise HTTPException(status_code=500, detail="アラートの承認に失敗しました")


@router.post("/{alert_id}/resolve")
async def resolve_alert(
    alert_id: str,
    db: Session = Depends(get_db)
):
    """アラートの解決"""
    try:
        service = AlertService(db)
        result = service.resolve_alert(alert_id)
        if not result:
            raise HTTPException(status_code=404, detail="アラートが見つかりません")
        return {"message": "アラートを解決しました"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"アラート解決エラー: {e}")
        raise HTTPException(status_code=500, detail="アラートの解決に失敗しました")

