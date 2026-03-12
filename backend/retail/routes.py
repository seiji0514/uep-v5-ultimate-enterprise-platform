"""
小売・EC APIエンドポイント
POS、EC、在庫、顧客分析
"""
from datetime import datetime, timedelta
from typing import Any, Dict, List

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/retail", tags=["小売・EC"])


def _pos_transactions() -> List[Dict[str, Any]]:
    return [
        {
            "id": "pos-001",
            "store": "店舗A",
            "amount": 3500,
            "items": 3,
            "timestamp": (datetime.utcnow() - timedelta(minutes=5)).isoformat(),
            "payment": "カード",
        },
        {
            "id": "pos-002",
            "store": "店舗B",
            "amount": 12800,
            "items": 5,
            "timestamp": (datetime.utcnow() - timedelta(minutes=12)).isoformat(),
            "payment": "現金",
        },
        {
            "id": "pos-003",
            "store": "店舗A",
            "amount": 5200,
            "items": 2,
            "timestamp": (datetime.utcnow() - timedelta(minutes=18)).isoformat(),
            "payment": "QR",
        },
        {
            "id": "pos-004",
            "store": "店舗C",
            "amount": 8900,
            "items": 4,
            "timestamp": (datetime.utcnow() - timedelta(minutes=25)).isoformat(),
            "payment": "カード",
        },
        {
            "id": "pos-005",
            "store": "店舗B",
            "amount": 2100,
            "items": 1,
            "timestamp": (datetime.utcnow() - timedelta(minutes=30)).isoformat(),
            "payment": "現金",
        },
        {
            "id": "pos-006",
            "store": "店舗A",
            "amount": 15600,
            "items": 6,
            "timestamp": (datetime.utcnow() - timedelta(minutes=35)).isoformat(),
            "payment": "カード",
        },
    ]


def _ec_orders() -> List[Dict[str, Any]]:
    return [
        {
            "id": "ec-001",
            "customer_id": "C001",
            "amount": 8500,
            "status": "発送済",
            "ordered_at": (datetime.utcnow() - timedelta(days=1)).isoformat(),
        },
        {
            "id": "ec-002",
            "customer_id": "C002",
            "amount": 3200,
            "status": "出荷準備中",
            "ordered_at": (datetime.utcnow() - timedelta(hours=5)).isoformat(),
        },
        {
            "id": "ec-003",
            "customer_id": "C003",
            "amount": 12500,
            "status": "入金確認",
            "ordered_at": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
        },
        {
            "id": "ec-004",
            "customer_id": "C001",
            "amount": 4500,
            "status": "発送済",
            "ordered_at": (datetime.utcnow() - timedelta(days=2)).isoformat(),
        },
        {
            "id": "ec-005",
            "customer_id": "C004",
            "amount": 9800,
            "status": "キャンセル",
            "ordered_at": (datetime.utcnow() - timedelta(hours=1)).isoformat(),
        },
        {
            "id": "ec-006",
            "customer_id": "C005",
            "amount": 21000,
            "status": "出荷準備中",
            "ordered_at": (datetime.utcnow() - timedelta(hours=8)).isoformat(),
        },
    ]


def _inventory_retail() -> List[Dict[str, Any]]:
    return [
        {
            "sku": "R-1001",
            "name": "商品A",
            "qty": 120,
            "reorder_level": 50,
            "status": "正常",
            "store": "倉庫中央",
        },
        {
            "sku": "R-1002",
            "name": "商品B",
            "qty": 35,
            "reorder_level": 40,
            "status": "要発注",
            "store": "倉庫中央",
        },
        {
            "sku": "R-1003",
            "name": "商品C",
            "qty": 250,
            "reorder_level": 80,
            "status": "正常",
            "store": "倉庫東",
        },
        {
            "sku": "R-1004",
            "name": "商品D",
            "qty": 18,
            "reorder_level": 30,
            "status": "要発注",
            "store": "倉庫西",
        },
        {
            "sku": "R-1005",
            "name": "商品E",
            "qty": 420,
            "reorder_level": 100,
            "status": "正常",
            "store": "倉庫中央",
        },
    ]


def _customer_analytics() -> List[Dict[str, Any]]:
    return [
        {"segment": "VIP", "count": 150, "avg_order": 25000, "ltv": 180000},
        {"segment": "リピーター", "count": 1200, "avg_order": 8500, "ltv": 45000},
        {"segment": "新規", "count": 800, "avg_order": 3200, "ltv": 8500},
        {"segment": "休眠", "count": 500, "avg_order": 0, "ltv": 12000},
    ]


@router.get("/pos-transactions")
async def get_pos_transactions():
    """POS取引一覧"""
    return {"items": _pos_transactions(), "total": len(_pos_transactions())}


@router.get("/ec-orders")
async def get_ec_orders():
    """EC注文一覧"""
    return {"items": _ec_orders(), "total": len(_ec_orders())}


@router.get("/inventory")
async def get_inventory():
    """小売在庫一覧"""
    return {"items": _inventory_retail(), "total": len(_inventory_retail())}


@router.get("/customer-analytics")
async def get_customer_analytics():
    """顧客セグメント分析"""
    return {"items": _customer_analytics(), "total": len(_customer_analytics())}


@router.get("/dashboard")
async def get_dashboard():
    """ダッシュボードサマリ"""
    pos = _pos_transactions()
    ec = _ec_orders()
    inv = _inventory_retail()
    return {
        "pos_today_sales": sum(p["amount"] for p in pos),
        "ec_orders_pending": len([e for e in ec if e["status"] in ["入金確認", "出荷準備中"]]),
        "inventory_reorder_count": len([i for i in inv if i["status"] == "要発注"]),
    }
