"""
金融・FinTech APIエンドポイント
決済API、リスクスコア、取引監視
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from fastapi import APIRouter, Depends

from auth.jwt_auth import get_current_active_user

router = APIRouter(prefix="/api/v1/fintech", tags=["金融・FinTech"])


def _payment_list() -> List[Dict[str, Any]]:
    return [
        {
            "id": "pay-001",
            "amount": 15000,
            "currency": "JPY",
            "status": "完了",
            "created_at": (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat(),
            "method": "credit",
        },
        {
            "id": "pay-002",
            "amount": 8500,
            "currency": "JPY",
            "status": "処理中",
            "created_at": (datetime.now(timezone.utc) - timedelta(minutes=2)).isoformat(),
            "method": "bank",
        },
        {
            "id": "pay-003",
            "amount": 32000,
            "currency": "JPY",
            "status": "完了",
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
            "method": "credit",
        },
        {
            "id": "pay-004",
            "amount": 5200,
            "currency": "JPY",
            "status": "完了",
            "created_at": (datetime.now(timezone.utc) - timedelta(minutes=25)).isoformat(),
            "method": "qr",
        },
        {
            "id": "pay-005",
            "amount": 98000,
            "currency": "JPY",
            "status": "処理中",
            "created_at": (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat(),
            "method": "bank",
        },
        {
            "id": "pay-006",
            "amount": 45000,
            "currency": "JPY",
            "status": "完了",
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
            "method": "credit",
        },
    ]


def _risk_scores() -> List[Dict[str, Any]]:
    return [
        {
            "transaction_id": "tx-001",
            "risk_score": 0.12,
            "level": "低",
            "factors": ["通常取引パターン"],
        },
        {
            "transaction_id": "tx-002",
            "risk_score": 0.45,
            "level": "中",
            "factors": ["新規送金先", "高額"],
        },
        {
            "transaction_id": "tx-003",
            "risk_score": 0.88,
            "level": "高",
            "factors": ["異常時間帯", "海外送金", "高額"],
        },
        {
            "transaction_id": "tx-004",
            "risk_score": 0.08,
            "level": "低",
            "factors": ["通常取引"],
        },
        {
            "transaction_id": "tx-005",
            "risk_score": 0.62,
            "level": "中",
            "factors": ["新規加盟店", "高額"],
        },
        {
            "transaction_id": "tx-006",
            "risk_score": 0.95,
            "level": "高",
            "factors": ["複数回失敗", "異常IP", "高額"],
        },
    ]


def _transaction_monitoring() -> List[Dict[str, Any]]:
    return [
        {
            "id": "mon-001",
            "type": "送金",
            "amount": 500000,
            "status": "監視中",
            "alert": "高額送金",
        },
        {"id": "mon-002", "type": "決済", "amount": 12000, "status": "正常", "alert": None},
        {
            "id": "mon-003",
            "type": "海外送金",
            "amount": 200000,
            "status": "要確認",
            "alert": "新規宛先",
        },
        {
            "id": "mon-004",
            "type": "送金",
            "amount": 350000,
            "status": "監視中",
            "alert": "高額送金",
        },
        {"id": "mon-005", "type": "決済", "amount": 8500, "status": "正常", "alert": None},
        {
            "id": "mon-006",
            "type": "海外送金",
            "amount": 150000,
            "status": "要確認",
            "alert": "新規宛先",
        },
    ]


@router.get("/payments")
async def get_payments(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """決済一覧を取得"""
    return {"items": _payment_list(), "total": len(_payment_list())}


@router.get("/risk-scores")
async def get_risk_scores(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """リスクスコア一覧を取得"""
    return {"items": _risk_scores(), "total": len(_risk_scores())}


@router.get("/stress-test")
async def run_stress_test(
    portfolio_value: float = 1000000,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """ストレステスト実行（規制対応）"""
    from fintech.stress_test import DEFAULT_SCENARIOS
    from fintech.stress_test import run_stress_test as _run

    return _run(portfolio_value=portfolio_value, scenarios=DEFAULT_SCENARIOS)


@router.get("/transaction-monitoring")
async def get_transaction_monitoring(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """取引監視一覧を取得"""
    return {"items": _transaction_monitoring(), "total": len(_transaction_monitoring())}
