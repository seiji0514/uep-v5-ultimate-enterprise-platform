"""
法務 APIエンドポイント
契約書レビュー、規制対応、知的財産、コンプライアンス
"""
from datetime import datetime, timedelta, timezone

from typing import Any, Dict, List

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/legal", tags=["法務"])


def _contract_reviews() -> List[Dict[str, Any]]:
    return [
        {
            "id": "cr-001",
            "title": "業務委託契約書",
            "status": "レビュー中",
            "risk_level": "中",
            "submitted_at": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
        },
        {
            "id": "cr-002",
            "title": "NDA（秘密保持契約）",
            "status": "承認済",
            "risk_level": "低",
            "submitted_at": (datetime.now(timezone.utc) - timedelta(days=3)).isoformat(),
        },
        {
            "id": "cr-003",
            "title": "ライセンス契約",
            "status": "要修正",
            "risk_level": "高",
            "submitted_at": (datetime.now(timezone.utc) - timedelta(days=2)).isoformat(),
        },
        {
            "id": "cr-004",
            "title": "販売代理店契約",
            "status": "レビュー中",
            "risk_level": "中",
            "submitted_at": (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat(),
        },
        {
            "id": "cr-005",
            "title": "SaaS利用規約",
            "status": "承認済",
            "risk_level": "低",
            "submitted_at": (datetime.now(timezone.utc) - timedelta(days=5)).isoformat(),
        },
    ]


def _regulatory_items() -> List[Dict[str, Any]]:
    return [
        {
            "id": "reg-001",
            "name": "個人情報保護法",
            "deadline": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
            "status": "対応中",
        },
        {
            "id": "reg-002",
            "name": "電子帳簿保存法",
            "deadline": (datetime.now(timezone.utc) + timedelta(days=60)).isoformat(),
            "status": "未着手",
        },
        {
            "id": "reg-003",
            "name": "サイバーセキュリティ経営ガイドライン",
            "deadline": (datetime.now(timezone.utc) + timedelta(days=14)).isoformat(),
            "status": "対応中",
        },
        {
            "id": "reg-004",
            "name": "労働基準法 年次有給",
            "deadline": (datetime.now(timezone.utc) + timedelta(days=90)).isoformat(),
            "status": "完了",
        },
    ]


def _ip_portfolio() -> List[Dict[str, Any]]:
    return [
        {
            "id": "ip-001",
            "type": "特許",
            "title": "AI分析手法",
            "status": "出願中",
            "filing_date": "2025-01-15",
        },
        {
            "id": "ip-002",
            "type": "商標",
            "title": "ブランドロゴ",
            "status": "登録済",
            "filing_date": "2024-06-01",
        },
        {
            "id": "ip-003",
            "type": "著作権",
            "title": "ソフトウェア",
            "status": "登録済",
            "filing_date": "2024-03-10",
        },
        {
            "id": "ip-004",
            "type": "特許",
            "title": "データ処理システム",
            "status": "審査中",
            "filing_date": "2025-02-20",
        },
    ]


def _compliance_alerts() -> List[Dict[str, Any]]:
    return [
        {
            "id": "ca-001",
            "type": "契約期限",
            "title": "業務委託契約 更新期限",
            "severity": "高",
            "due_date": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
        },
        {
            "id": "ca-002",
            "type": "規制対応",
            "title": "個人情報保護法 社内教育",
            "severity": "中",
            "due_date": (datetime.now(timezone.utc) + timedelta(days=14)).isoformat(),
        },
        {
            "id": "ca-003",
            "type": "監査",
            "title": "内部監査 実施",
            "severity": "中",
            "due_date": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
        },
    ]


@router.get("/contract-reviews")
async def get_contract_reviews():
    """契約書レビュー一覧"""
    return {"items": _contract_reviews(), "total": len(_contract_reviews())}


@router.get("/regulatory")
async def get_regulatory():
    """規制対応一覧"""
    return {"items": _regulatory_items(), "total": len(_regulatory_items())}


@router.get("/ip-portfolio")
async def get_ip_portfolio():
    """知的財産ポートフォリオ"""
    return {"items": _ip_portfolio(), "total": len(_ip_portfolio())}


@router.get("/compliance-alerts")
async def get_compliance_alerts():
    """コンプライアンスアラート"""
    return {"items": _compliance_alerts(), "total": len(_compliance_alerts())}


@router.get("/dashboard")
async def get_dashboard():
    """ダッシュボードサマリ"""
    contracts = _contract_reviews()
    regs = _regulatory_items()
    ip_list = _ip_portfolio()
    return {
        "contracts_pending": len(
            [c for c in contracts if c["status"] in ["レビュー中", "要修正"]]
        ),
        "regulatory_due_soon": len([r for r in regs if r["status"] != "完了"]),
        "ip_pending": len([i for i in ip_list if i["status"] in ["出願中", "審査中"]]),
    }
