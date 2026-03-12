"""
ESGレポートAPI
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.core.database import get_db
from app.services.esg_service import ESGService
from loguru import logger

router = APIRouter()


@router.get("/reports")
async def get_esg_reports(
    report_type: str = None,
    period_start: Optional[date] = None,
    period_end: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """ESGレポート一覧の取得"""
    try:
        service = ESGService(db)
        reports = service.get_esg_reports(
            report_type=report_type,
            period_start=period_start,
            period_end=period_end,
            skip=skip,
            limit=limit
        )
        return reports
    except Exception as e:
        logger.error(f"ESGレポート一覧取得エラー: {e}")
        raise HTTPException(status_code=500, detail="ESGレポート一覧の取得に失敗しました")


@router.post("/reports/generate")
async def generate_esg_report(
    report_type: str,
    period_start: date,
    period_end: date,
    db: Session = Depends(get_db)
):
    """ESGレポートの自動生成"""
    try:
        service = ESGService(db)
        report = service.generate_esg_report(
            report_type=report_type,
            period_start=period_start,
            period_end=period_end
        )
        return report
    except Exception as e:
        logger.error(f"ESGレポート生成エラー: {e}")
        raise HTTPException(status_code=500, detail="ESGレポートの生成に失敗しました")


@router.get("/carbon-footprint")
async def get_carbon_footprint(
    period_start: Optional[date] = None,
    period_end: Optional[date] = None,
    scope: str = None,
    db: Session = Depends(get_db)
):
    """カーボンフットプリントの取得"""
    try:
        service = ESGService(db)
        carbon_footprint = service.get_carbon_footprint(
            period_start=period_start,
            period_end=period_end,
            scope=scope
        )
        return carbon_footprint
    except Exception as e:
        logger.error(f"カーボンフットプリント取得エラー: {e}")
        raise HTTPException(status_code=500, detail="カーボンフットプリントの取得に失敗しました")


@router.post("/carbon-footprint")
async def create_carbon_footprint(
    period_start: date,
    period_end: date,
    scope: str,
    category: str,
    value: float,
    unit: str = "tCO2e",
    db: Session = Depends(get_db)
):
    """カーボンフットプリントの作成"""
    try:
        service = ESGService(db)
        result = service.create_carbon_footprint(
            period_start=period_start,
            period_end=period_end,
            scope=scope,
            category=category,
            value=value,
            unit=unit
        )
        return result
    except Exception as e:
        logger.error(f"カーボンフットプリント作成エラー: {e}")
        raise HTTPException(status_code=500, detail="カーボンフットプリントの作成に失敗しました")

