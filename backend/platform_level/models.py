"""
Level 2 プラットフォーム - Pydanticモデル
"""
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class TenantStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TRIAL = "trial"


class TenantCreate(BaseModel):
    name: str
    organization: str
    plan_id: str
    contact_email: str


class Tenant(BaseModel):
    id: str
    name: str
    organization: str
    plan_id: str
    status: str
    contact_email: str
    created_at: str
    resource_limits: Optional[Dict[str, Any]] = None


class SubscriptionPlan(BaseModel):
    id: str
    name: str
    price_monthly: float
    features: List[str]
    api_calls_limit: int
    storage_gb: int


class ApiListing(BaseModel):
    id: str
    name: str
    description: str
    endpoint: str
    provider_tenant_id: str
    price_per_call: float
    category: str
    created_at: str
    call_count: int = 0
