"""
公共・官公庁 APIエンドポイント
申請・承認ワークフロー、マイナンバー連携、自治体向け
"""
from datetime import datetime, timedelta
from typing import Any, Dict, List

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/public-sector", tags=["公共・官公庁"])


def _applications() -> List[Dict[str, Any]]:
    return [
        {
            "id": "app-001",
            "type": "住民票",
            "applicant": "市民A",
            "status": "申請中",
            "submitted_at": (datetime.utcnow() - timedelta(days=1)).isoformat(),
            "office": "区役所",
        },
        {
            "id": "app-002",
            "type": "戸籍抄本",
            "applicant": "市民B",
            "status": "承認済",
            "submitted_at": (datetime.utcnow() - timedelta(days=3)).isoformat(),
            "office": "市役所",
        },
        {
            "id": "app-003",
            "type": "印鑑証明",
            "applicant": "市民C",
            "status": "差し戻し",
            "submitted_at": (datetime.utcnow() - timedelta(days=2)).isoformat(),
            "office": "区役所",
        },
        {
            "id": "app-004",
            "type": "マイナンバーカード",
            "applicant": "市民D",
            "status": "申請中",
            "submitted_at": (datetime.utcnow() - timedelta(hours=5)).isoformat(),
            "office": "市役所",
        },
        {
            "id": "app-005",
            "type": "補助金申請",
            "applicant": "法人E",
            "status": "審査中",
            "submitted_at": (datetime.utcnow() - timedelta(days=5)).isoformat(),
            "office": "経済課",
        },
        {
            "id": "app-006",
            "type": "建築確認",
            "applicant": "法人F",
            "status": "承認済",
            "submitted_at": (datetime.utcnow() - timedelta(days=7)).isoformat(),
            "office": "建築課",
        },
    ]


def _approval_workflow() -> List[Dict[str, Any]]:
    return [
        {
            "id": "wf-001",
            "title": "予算執行承認",
            "current_step": "課長承認",
            "status": "進行中",
            "deadline": (datetime.utcnow() + timedelta(days=3)).isoformat(),
        },
        {
            "id": "wf-002",
            "title": "契約締結承認",
            "current_step": "部長承認",
            "status": "進行中",
            "deadline": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        },
        {
            "id": "wf-003",
            "title": "入札結果承認",
            "current_step": "完了",
            "status": "完了",
            "deadline": (datetime.utcnow() - timedelta(days=1)).isoformat(),
        },
        {
            "id": "wf-004",
            "title": "情報公開請求対応",
            "current_step": "担当確認",
            "status": "進行中",
            "deadline": (datetime.utcnow() + timedelta(days=5)).isoformat(),
        },
    ]


def _mynumber_stats() -> List[Dict[str, Any]]:
    return [
        {"metric": "カード交付件数", "value": 1250, "unit": "件/月", "trend": "増加"},
        {"metric": "電子申請利用", "value": 3400, "unit": "件/月", "trend": "増加"},
        {"metric": "窓口来庁", "value": 8200, "unit": "件/月", "trend": "減少"},
    ]


@router.get("/applications")
async def get_applications():
    """申請一覧"""
    return {"items": _applications(), "total": len(_applications())}


@router.get("/approval-workflow")
async def get_approval_workflow():
    """承認ワークフロー一覧"""
    return {"items": _approval_workflow(), "total": len(_approval_workflow())}


@router.get("/mynumber-stats")
async def get_mynumber_stats():
    """マイナンバー関連統計"""
    return {"items": _mynumber_stats(), "total": len(_mynumber_stats())}


@router.get("/dashboard")
async def get_dashboard():
    """ダッシュボードサマリ"""
    apps = _applications()
    return {
        "applications_pending": len([a for a in apps if a["status"] in ["申請中", "審査中"]]),
        "applications_approved": len([a for a in apps if a["status"] == "承認済"]),
        "workflow_in_progress": len(
            [w for w in _approval_workflow() if w["status"] == "進行中"]
        ),
    }
