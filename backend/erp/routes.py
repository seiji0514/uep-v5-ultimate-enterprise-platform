"""
ERP（統合基幹業務システム）API
販売管理・購買管理・データ連携基盤
"""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from auth.jwt_auth import get_current_active_user
from auth.rbac import require_permission

from .data_integration import data_integration_manager
from .models import (
    DataSyncRuleCreate,
    PurchaseOrderCreate,
    PurchaseOrderUpdate,
    SalesOrderCreate,
    SalesOrderUpdate,
)
from .purchasing import purchasing_manager
from .sales import sales_manager

router = APIRouter(prefix="/api/v1/erp", tags=["ERP（統合基幹業務システム）"])


# ========== サマリー・ヘルス ==========


@router.get("/summary")
@require_permission("read")
async def get_erp_summary(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """ERP統合サマリー"""
    sales = sales_manager.get_sales_summary()
    purchasing = purchasing_manager.get_purchasing_summary()
    integration = data_integration_manager.get_summary()
    return {
        "platform": "ERP（統合基幹業務システム）",
        "version": "1.0.0",
        "modules": {
            "販売管理": {
                "order_count": sales["order_count"],
                "total_sales": sales["total_sales"],
            },
            "購買管理": {
                "order_count": purchasing["order_count"],
                "total_purchases": purchasing["total_purchases"],
            },
            "データ連携": integration,
        },
    }


# ========== 販売管理 ==========


@router.post("/sales/orders", response_model=Dict[str, Any])
@require_permission("write")
async def create_sales_order(
    body: SalesOrderCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """受注作成"""
    return sales_manager.create_order(
        customer_id=body.customer_id,
        customer_name=body.customer_name,
        items=body.items,
        total_amount=body.total_amount,
        notes=body.notes,
    )


@router.get("/sales/orders", response_model=List[Dict[str, Any]])
@require_permission("read")
async def list_sales_orders(
    status: Optional[str] = None,
    limit: int = 100,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """受注一覧"""
    return sales_manager.list_orders(status=status, limit=limit)


@router.get("/sales/orders/{order_id}")
@require_permission("read")
async def get_sales_order(
    order_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """受注詳細"""
    order = sales_manager.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/sales/orders/{order_id}")
@require_permission("write")
async def update_sales_order(
    order_id: str,
    body: SalesOrderUpdate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """受注更新"""
    order = sales_manager.update_order(
        order_id,
        status=body.status.value if body.status else None,
        shipped_at=body.shipped_at,
        invoice_no=body.invoice_no,
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# ========== 購買管理 ==========


@router.post("/purchasing/orders", response_model=Dict[str, Any])
@require_permission("write")
async def create_purchase_order(
    body: PurchaseOrderCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """発注作成"""
    return purchasing_manager.create_order(
        supplier_id=body.supplier_id,
        supplier_name=body.supplier_name,
        items=body.items,
        total_amount=body.total_amount,
        notes=body.notes,
    )


@router.get("/purchasing/orders", response_model=List[Dict[str, Any]])
@require_permission("read")
async def list_purchase_orders(
    status: Optional[str] = None,
    limit: int = 100,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """発注一覧"""
    return purchasing_manager.list_orders(status=status, limit=limit)


@router.get("/purchasing/orders/{order_id}")
@require_permission("read")
async def get_purchase_order(
    order_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """発注詳細"""
    order = purchasing_manager.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/purchasing/orders/{order_id}")
@require_permission("write")
async def update_purchase_order(
    order_id: str,
    body: PurchaseOrderUpdate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """発注更新"""
    order = purchasing_manager.update_order(
        order_id,
        status=body.status.value if body.status else None,
        received_at=body.received_at,
        invoice_no=body.invoice_no,
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# ========== データ連携基盤 ==========


@router.post("/data-integration/rules", response_model=Dict[str, Any])
@require_permission("write")
async def create_sync_rule(
    body: DataSyncRuleCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """データ連携ルール作成"""
    return data_integration_manager.create_rule(
        source=body.source_system,
        target=body.target_system,
        sync_type=body.sync_type,
        schedule=body.schedule,
        mapping=body.mapping,
    )


@router.get("/data-integration/rules", response_model=List[Dict[str, Any]])
@require_permission("read")
async def list_sync_rules(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """データ連携ルール一覧"""
    return data_integration_manager.list_rules()


@router.post("/data-integration/sync/{rule_id}")
@require_permission("write")
async def execute_sync(
    rule_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """データ連携実行"""
    return data_integration_manager.execute_sync(rule_id)


@router.get("/data-integration/logs", response_model=List[Dict[str, Any]])
@require_permission("read")
async def get_sync_logs(
    limit: int = 50,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """データ連携ログ"""
    return data_integration_manager.get_sync_logs(limit=limit)
