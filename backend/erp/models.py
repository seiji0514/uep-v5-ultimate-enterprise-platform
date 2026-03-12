"""
ERP - Pydanticモデル
販売管理・購買管理
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

# ========== 販売管理 ==========


class SalesOrderStatus(str, Enum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    INVOICED = "invoiced"
    PAID = "paid"
    CANCELLED = "cancelled"


class SalesOrderCreate(BaseModel):
    """受注作成"""

    customer_id: str
    customer_name: str
    items: List[Dict[str, Any]]  # [{product_id, product_name, quantity, unit_price}]
    total_amount: float
    notes: Optional[str] = None


class SalesOrderUpdate(BaseModel):
    """受注更新"""

    status: Optional[SalesOrderStatus] = None
    shipped_at: Optional[str] = None
    invoice_no: Optional[str] = None


# ========== 購買管理 ==========


class PurchaseOrderStatus(str, Enum):
    DRAFT = "draft"
    APPROVED = "approved"
    ORDERED = "ordered"
    RECEIVED = "received"
    PAID = "paid"
    CANCELLED = "cancelled"


class PurchaseOrderCreate(BaseModel):
    """発注作成"""

    supplier_id: str
    supplier_name: str
    items: List[Dict[str, Any]]  # [{product_id, product_name, quantity, unit_price}]
    total_amount: float
    notes: Optional[str] = None


class PurchaseOrderUpdate(BaseModel):
    """発注更新"""

    status: Optional[PurchaseOrderStatus] = None
    received_at: Optional[str] = None
    invoice_no: Optional[str] = None


# ========== データ連携 ==========


class DataSyncRuleCreate(BaseModel):
    """データ連携ルール作成"""

    source_system: str  # erp_sales, erp_purchasing, accounting, hr
    target_system: str
    sync_type: str  # realtime, batch
    schedule: Optional[str] = None  # cron式（batchの場合）
    mapping: Optional[Dict[str, str]] = None  # フィールドマッピング
