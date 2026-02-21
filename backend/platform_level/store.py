"""
Level 2 プラットフォーム - インメモリストア
"""
import uuid
from datetime import datetime
from typing import Dict, List, Optional


class PlatformStore:
    """プラットフォームデータのインメモリストア"""

    def __init__(self):
        self.tenants: Dict[str, dict] = {}
        self.plans: Dict[str, dict] = {}
        self.api_listings: Dict[str, dict] = {}
        self._init_demo_data()

    def _init_demo_data(self):
        """デモ用初期データ"""
        plans = [
            {
                "id": "free",
                "name": "Free",
                "price_monthly": 0,
                "features": ["基本API", "1GBストレージ"],
                "api_calls_limit": 1000,
                "storage_gb": 1,
            },
            {
                "id": "starter",
                "name": "Starter",
                "price_monthly": 9900,
                "features": ["全API", "10GBストレージ", "サポート"],
                "api_calls_limit": 10000,
                "storage_gb": 10,
            },
            {
                "id": "pro",
                "name": "Pro",
                "price_monthly": 49900,
                "features": ["全API", "100GBストレージ", "優先サポート", "SLA 99.9%"],
                "api_calls_limit": 100000,
                "storage_gb": 100,
            },
            {
                "id": "enterprise",
                "name": "Enterprise",
                "price_monthly": 199000,
                "features": ["全API", "無制限", "専用サポート", "SLA 99.99%", "カスタム統合"],
                "api_calls_limit": -1,
                "storage_gb": 1000,
            },
        ]
        for p in plans:
            self.plans[p["id"]] = p

        t1 = {
            "id": "tenant-001",
            "name": "Demo Corp",
            "organization": "Demo Corporation",
            "plan_id": "pro",
            "status": "active",
            "contact_email": "admin@demo.example.com",
            "created_at": datetime.utcnow().isoformat(),
            "resource_limits": {"api_calls": 100000, "storage_gb": 100},
        }
        self.tenants[t1["id"]] = t1

        a1 = {
            "id": "api-001",
            "name": "UEP MLOps API",
            "description": "MLOps パイプライン・モデル管理API",
            "endpoint": "/api/v1/mlops",
            "provider_tenant_id": "tenant-001",
            "price_per_call": 0.1,
            "category": "mlops",
            "created_at": datetime.utcnow().isoformat(),
            "call_count": 1250,
        }
        self.api_listings[a1["id"]] = a1

    def create_tenant(self, data: dict) -> dict:
        tid = f"tenant-{uuid.uuid4().hex[:8]}"
        plan = self.plans.get(data["plan_id"], self.plans["free"])
        data["id"] = tid
        data["status"] = "active"
        data["created_at"] = datetime.utcnow().isoformat()
        data["resource_limits"] = {
            "api_calls": plan["api_calls_limit"],
            "storage_gb": plan["storage_gb"],
        }
        self.tenants[tid] = data
        return data

    def list_tenants(self) -> List[dict]:
        return list(self.tenants.values())

    def get_tenant(self, tenant_id: str) -> Optional[dict]:
        return self.tenants.get(tenant_id)

    def list_plans(self) -> List[dict]:
        return list(self.plans.values())

    def create_api_listing(self, data: dict) -> dict:
        aid = f"api-{uuid.uuid4().hex[:8]}"
        data["id"] = aid
        data["created_at"] = datetime.utcnow().isoformat()
        data["call_count"] = 0
        self.api_listings[aid] = data
        return data

    def list_api_listings(self, category: Optional[str] = None) -> List[dict]:
        items = list(self.api_listings.values())
        if category:
            items = [a for a in items if a["category"] == category]
        return items


platform_store = PlatformStore()
