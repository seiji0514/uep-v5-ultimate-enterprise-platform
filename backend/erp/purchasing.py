"""
ERP - 購買管理
発注・入荷・支払・仕入集計
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import PurchaseOrderStatus


class PurchasingManager:
    """購買管理マネージャー"""

    _orders: Dict[str, Dict[str, Any]]

    def __init__(self):
        self._orders = {}

    def create_order(
        self,
        supplier_id: str,
        supplier_name: str,
        items: List[Dict],
        total_amount: float,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        order_id = (
            f"PO-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
        )
        order = {
            "id": order_id,
            "supplier_id": supplier_id,
            "supplier_name": supplier_name,
            "items": items,
            "total_amount": total_amount,
            "status": PurchaseOrderStatus.DRAFT.value,
            "notes": notes,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        self._orders[order_id] = order
        return order

    def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        return self._orders.get(order_id)

    def list_orders(
        self, status: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        orders = list(self._orders.values())
        if status:
            orders = [o for o in orders if o["status"] == status]
        return sorted(orders, key=lambda x: x["created_at"], reverse=True)[:limit]

    def update_order(
        self,
        order_id: str,
        status: Optional[str] = None,
        received_at: Optional[str] = None,
        invoice_no: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        order = self._orders.get(order_id)
        if not order:
            return None
        if status:
            order["status"] = status
        if received_at:
            order["received_at"] = received_at
        if invoice_no:
            order["invoice_no"] = invoice_no
        order["updated_at"] = datetime.utcnow().isoformat()
        return order

    def get_purchasing_summary(self) -> Dict[str, Any]:
        total = sum(
            o["total_amount"]
            for o in self._orders.values()
            if o["status"] != PurchaseOrderStatus.CANCELLED.value
        )
        count = len(
            [
                o
                for o in self._orders.values()
                if o["status"] != PurchaseOrderStatus.CANCELLED.value
            ]
        )
        return {"total_purchases": total, "order_count": count, "orders": self._orders}


purchasing_manager = PurchasingManager()
