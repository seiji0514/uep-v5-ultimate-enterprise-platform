"""
統括責任者向けダッシュボードAPI
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.core.database import get_db
from app.services.dashboard_service import DashboardService
from loguru import logger

router = APIRouter()


@router.get("/overview")
async def get_dashboard_overview(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """ダッシュボード概要の取得"""
    try:
        service = DashboardService(db)
        overview = await service.get_dashboard_overview(
            start_time=start_time,
            end_time=end_time
        )
        return overview
    except Exception as e:
        logger.error(f"ダッシュボード概要取得エラー: {e}")
        raise HTTPException(status_code=500, detail="ダッシュボード概要の取得に失敗しました")


@router.get("/kpi")
async def get_dashboard_kpi(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """統合KPIの取得"""
    try:
        service = DashboardService(db)
        kpi = service.get_dashboard_kpi(
            start_time=start_time,
            end_time=end_time
        )
        return kpi
    except Exception as e:
        logger.error(f"統合KPI取得エラー: {e}")
        raise HTTPException(status_code=500, detail="統合KPIの取得に失敗しました")


@router.get("/alerts-summary")
async def get_alerts_summary(
    severity: str = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """アラートサマリーの取得"""
    try:
        service = DashboardService(db)
        alerts_summary = service.get_alerts_summary(
            severity=severity,
            status=status
        )
        return alerts_summary
    except Exception as e:
        logger.error(f"アラートサマリー取得エラー: {e}")
        raise HTTPException(status_code=500, detail="アラートサマリーの取得に失敗しました")

