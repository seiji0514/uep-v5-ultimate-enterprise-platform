"""
判断支援API
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.core.database import get_db
from app.services.decision_support_service import DecisionSupportService
from loguru import logger

router = APIRouter()


@router.post("/scenario-analysis")
async def perform_scenario_analysis(
    scenario_type: str,
    parameters: dict,
    user_id: str,
    db: Session = Depends(get_db)
):
    """シナリオ分析の実行"""
    try:
        service = DecisionSupportService(db)
        analysis = service.perform_scenario_analysis(
            scenario_type=scenario_type,
            parameters=parameters,
            user_id=user_id
        )
        return analysis
    except Exception as e:
        logger.error(f"シナリオ分析エラー: {e}")
        raise HTTPException(status_code=500, detail="シナリオ分析の実行に失敗しました")


@router.post("/risk-assessment")
async def perform_risk_assessment(
    assessment_type: str,
    parameters: dict,
    user_id: str,
    db: Session = Depends(get_db)
):
    """リスク評価の実行"""
    try:
        service = DecisionSupportService(db)
        assessment = service.perform_risk_assessment(
            assessment_type=assessment_type,
            parameters=parameters,
            user_id=user_id
        )
        return assessment
    except Exception as e:
        logger.error(f"リスク評価エラー: {e}")
        raise HTTPException(status_code=500, detail="リスク評価の実行に失敗しました")


@router.post("/generate-runbook")
async def generate_runbook(
    runbook_type: str,
    parameters: dict,
    user_id: str,
    db: Session = Depends(get_db)
):
    """Runbookの自動生成"""
    try:
        service = DecisionSupportService(db)
        runbook = service.generate_runbook(
            runbook_type=runbook_type,
            parameters=parameters,
            user_id=user_id
        )
        return runbook
    except Exception as e:
        logger.error(f"Runbook生成エラー: {e}")
        raise HTTPException(status_code=500, detail="Runbookの生成に失敗しました")


@router.get("/logs")
async def get_decision_support_logs(
    user_id: str = None,
    decision_type: str = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """判断支援ログの取得"""
    try:
        service = DecisionSupportService(db)
        logs = service.get_decision_support_logs(
            user_id=user_id,
            decision_type=decision_type,
            start_time=start_time,
            end_time=end_time,
            skip=skip,
            limit=limit
        )
        return logs
    except Exception as e:
        logger.error(f"判断支援ログ取得エラー: {e}")
        raise HTTPException(status_code=500, detail="判断支援ログの取得に失敗しました")

