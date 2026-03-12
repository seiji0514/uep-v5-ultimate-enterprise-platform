"""
サプライチェーン系 API
物流、在庫、調達
認証不要でデモ用サンプルデータを返す
"""
from datetime import datetime, timedelta
from typing import Any, Dict, List

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/supply-chain", tags=["サプライチェーン系"])


def _logistics_shipments() -> List[Dict[str, Any]]:
    return [
        {
            "id": "ship-001",
            "origin": "東京倉庫",
            "destination": "大阪配送",
            "status": "配送中",
            "eta": (datetime.utcnow() + timedelta(hours=4)).isoformat(),
            "carrier": "ヤマト",
        },
        {
            "id": "ship-002",
            "origin": "福岡倉庫",
            "destination": "名古屋配送",
            "status": "出荷済",
            "eta": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "carrier": "佐川",
        },
        {
            "id": "ship-003",
            "origin": "輸入港",
            "destination": "東京倉庫",
            "status": "通関中",
            "eta": (datetime.utcnow() + timedelta(days=2)).isoformat(),
            "carrier": "船便",
        },
        {
            "id": "ship-004",
            "origin": "大阪倉庫",
            "destination": "札幌配送",
            "status": "配送中",
            "eta": (datetime.utcnow() + timedelta(hours=18)).isoformat(),
            "carrier": "ヤマト",
        },
        {
            "id": "ship-005",
            "origin": "名古屋倉庫",
            "destination": "横浜配送",
            "status": "出荷済",
            "eta": (datetime.utcnow() + timedelta(hours=8)).isoformat(),
            "carrier": "西濃",
        },
        {
            "id": "ship-006",
            "origin": "横浜倉庫",
            "destination": "仙台配送",
            "status": "配送中",
            "eta": (datetime.utcnow() + timedelta(hours=12)).isoformat(),
            "carrier": "ヤマト",
        },
        {
            "id": "ship-007",
            "origin": "東京倉庫",
            "destination": "福岡配送",
            "status": "出荷済",
            "eta": (datetime.utcnow() + timedelta(days=2)).isoformat(),
            "carrier": "佐川",
        },
        {
            "id": "ship-008",
            "origin": "輸入港",
            "destination": "大阪倉庫",
            "status": "通関中",
            "eta": (datetime.utcnow() + timedelta(days=3)).isoformat(),
            "carrier": "船便",
        },
    ]


def _inventory_items() -> List[Dict[str, Any]]:
    return [
        {
            "id": "inv-001",
            "sku": "SKU-1001",
            "name": "部品A",
            "qty": 1250,
            "reorder_level": 500,
            "status": "正常",
            "warehouse": "東京",
        },
        {
            "id": "inv-002",
            "sku": "SKU-1002",
            "name": "部品B",
            "qty": 180,
            "reorder_level": 300,
            "status": "要発注",
            "warehouse": "東京",
        },
        {
            "id": "inv-003",
            "sku": "SKU-1003",
            "name": "部品C",
            "qty": 5200,
            "reorder_level": 1000,
            "status": "正常",
            "warehouse": "大阪",
        },
        {
            "id": "inv-004",
            "sku": "SKU-1004",
            "name": "部品D",
            "qty": 85,
            "reorder_level": 200,
            "status": "要発注",
            "warehouse": "名古屋",
        },
        {
            "id": "inv-005",
            "sku": "SKU-1005",
            "name": "部品E",
            "qty": 3200,
            "reorder_level": 800,
            "status": "正常",
            "warehouse": "東京",
        },
        {
            "id": "inv-006",
            "sku": "SKU-1006",
            "name": "部品F",
            "qty": 450,
            "reorder_level": 400,
            "status": "正常",
            "warehouse": "福岡",
        },
        {
            "id": "inv-007",
            "sku": "SKU-1007",
            "name": "部品G",
            "qty": 95,
            "reorder_level": 150,
            "status": "要発注",
            "warehouse": "大阪",
        },
        {
            "id": "inv-008",
            "sku": "SKU-1008",
            "name": "部品H",
            "qty": 2100,
            "reorder_level": 600,
            "status": "正常",
            "warehouse": "東京",
        },
    ]


def _procurement_orders() -> List[Dict[str, Any]]:
    return [
        {
            "id": "po-001",
            "supplier": "サプライヤーA",
            "amount": 500000,
            "status": "発注済",
            "delivery_date": (datetime.utcnow() + timedelta(days=7)).isoformat(),
            "items": 3,
        },
        {
            "id": "po-002",
            "supplier": "サプライヤーB",
            "amount": 320000,
            "status": "入荷待ち",
            "delivery_date": (datetime.utcnow() + timedelta(days=2)).isoformat(),
            "items": 5,
        },
        {
            "id": "po-003",
            "supplier": "サプライヤーC",
            "amount": 180000,
            "status": "入荷済",
            "delivery_date": (datetime.utcnow() - timedelta(days=1)).isoformat(),
            "items": 2,
        },
        {
            "id": "po-004",
            "supplier": "サプライヤーD",
            "amount": 450000,
            "status": "発注済",
            "delivery_date": (datetime.utcnow() + timedelta(days=10)).isoformat(),
            "items": 4,
        },
        {
            "id": "po-005",
            "supplier": "サプライヤーE",
            "amount": 280000,
            "status": "入荷待ち",
            "delivery_date": (datetime.utcnow() + timedelta(days=3)).isoformat(),
            "items": 6,
        },
        {
            "id": "po-006",
            "supplier": "サプライヤーF",
            "amount": 380000,
            "status": "発注済",
            "delivery_date": (datetime.utcnow() + timedelta(days=7)).isoformat(),
            "items": 8,
        },
        {
            "id": "po-007",
            "supplier": "サプライヤーG",
            "amount": 195000,
            "status": "入荷済",
            "delivery_date": (datetime.utcnow() - timedelta(days=2)).isoformat(),
            "items": 3,
        },
        {
            "id": "po-008",
            "supplier": "サプライヤーH",
            "amount": 520000,
            "status": "入荷待ち",
            "delivery_date": (datetime.utcnow() + timedelta(days=5)).isoformat(),
            "items": 10,
        },
    ]


def _demand_forecast() -> List[Dict[str, Any]]:
    return [
        {
            "sku": "SKU-1001",
            "period": "来週",
            "forecast": 800,
            "actual_last": 750,
            "accuracy": 0.94,
            "trend": "横ばい",
        },
        {
            "sku": "SKU-1002",
            "period": "来週",
            "forecast": 350,
            "actual_last": 320,
            "accuracy": 0.91,
            "trend": "増加",
        },
        {
            "sku": "SKU-1003",
            "period": "来週",
            "forecast": 1200,
            "actual_last": 1180,
            "accuracy": 0.98,
            "trend": "横ばい",
        },
        {
            "sku": "SKU-1004",
            "period": "来週",
            "forecast": 250,
            "actual_last": 240,
            "accuracy": 0.96,
            "trend": "減少",
        },
        {
            "sku": "SKU-1005",
            "period": "来週",
            "forecast": 950,
            "actual_last": 920,
            "accuracy": 0.97,
            "trend": "横ばい",
        },
        {
            "sku": "SKU-1006",
            "period": "来週",
            "forecast": 420,
            "actual_last": 410,
            "accuracy": 0.95,
            "trend": "増加",
        },
        {
            "sku": "SKU-1007",
            "period": "来週",
            "forecast": 180,
            "actual_last": 175,
            "accuracy": 0.92,
            "trend": "横ばい",
        },
        {
            "sku": "SKU-1008",
            "period": "来週",
            "forecast": 650,
            "actual_last": 630,
            "accuracy": 0.96,
            "trend": "増加",
        },
    ]


@router.get("/logistics-shipments")
async def get_logistics():
    return {"items": _logistics_shipments(), "total": len(_logistics_shipments())}


@router.get("/inventory-items")
async def get_inventory():
    return {"items": _inventory_items(), "total": len(_inventory_items())}


@router.get("/procurement-orders")
async def get_procurement():
    return {"items": _procurement_orders(), "total": len(_procurement_orders())}


@router.get("/demand-forecast")
async def get_demand_forecast():
    return {"items": _demand_forecast(), "total": len(_demand_forecast())}


@router.get("/dashboard")
async def get_dashboard():
    inv = _inventory_items()
    return {
        "shipments_in_transit": len(
            [s for s in _logistics_shipments() if s["status"] in ["配送中", "出荷済", "通関中"]]
        ),
        "inventory_reorder_count": len([i for i in inv if i["status"] == "要発注"]),
        "procurement_total": sum(p["amount"] for p in _procurement_orders()),
        "inventory_total_units": sum(i["qty"] for i in inv),
    }
