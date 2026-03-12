"""
AIガバナンス・ワークフロー API
ログ記録、リスク評価、監査
"""
from typing import Any, Dict

from fastapi import APIRouter, Depends

from auth.jwt_auth import get_current_active_user
from auth.rbac import require_permission

from .ai_usage_log import assess_risk, get_ai_usage_logs, log_ai_usage

router = APIRouter(prefix="/api/v1/governance", tags=["AIガバナンス"])


@router.get("/logs")
@require_permission("read")
async def get_logs(
    limit: int = 100,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """AI利用ログを取得（監査用）"""
    user_id = current_user.get("username", "")
    logs = get_ai_usage_logs(limit=limit, user_id=user_id)
    return {"logs": logs, "count": len(logs)}


@router.get("/logs/all")
@require_permission("read")
async def get_all_logs(
    limit: int = 100,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """全AI利用ログを取得（管理者用）"""
    logs = get_ai_usage_logs(limit=limit)
    return {"logs": logs, "count": len(logs)}


@router.post("/risk-assess")
@require_permission("read")
async def risk_assess(
    text: str,
    operation: str = "general",
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """入力テキストのリスクレベルを評価"""
    level = assess_risk(text, operation)
    return {
        "risk_level": level,
        "operation": operation,
        "description": {
            "low": "低リスク: 一般的な用途",
            "medium": "中リスク: 個人・評価関連の可能性",
            "high": "高リスク: 医療・法律・金融等の可能性",
        }.get(level, "不明"),
    }


@router.post("/log")
@require_permission("read")
async def record_usage(
    operation: str,
    model: str,
    input_summary: str = "",
    output_summary: str = "",
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """AI利用を手動でログ記録（他モジュールからの呼び出し用）"""
    risk = assess_risk(input_summary, operation)
    entry = log_ai_usage(
        operation=operation,
        model=model,
        user_id=current_user.get("username", ""),
        input_summary=input_summary,
        output_summary=output_summary,
        risk_level=risk,
    )
    return {"status": "logged", "entry": entry}
