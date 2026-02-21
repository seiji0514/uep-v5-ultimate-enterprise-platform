"""
統合ダッシュボードAPIエンドポイント
"""
from fastapi import APIRouter, Depends
from typing import Dict, Any
from .unified_dashboard import unified_dashboard
from .security_dashboard import security_dashboard
from .mlops_dashboard import mlops_dashboard
from auth.jwt_auth import get_current_active_user
from auth.rbac import require_permission

router = APIRouter(prefix="/api/v1/dashboards", tags=["ダッシュボード"])


@router.get("/unified")
@require_permission("read")
async def get_unified_dashboard(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """統合管理ダッシュボードデータを取得"""
    return unified_dashboard.get_dashboard_data()


@router.get("/security")
@require_permission("read")
async def get_security_dashboard(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """統合セキュリティダッシュボードデータを取得"""
    return security_dashboard.get_dashboard_data()


@router.get("/mlops")
@require_permission("read")
async def get_mlops_dashboard(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """統合MLOpsダッシュボードデータを取得"""
    return mlops_dashboard.get_dashboard_data()
