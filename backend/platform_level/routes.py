"""
Level 2 プラットフォーム - APIルート
マルチテナント、SaaS化、APIマーケットプレイス
"""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from auth.jwt_auth import get_current_active_user
from auth.rbac import require_permission

from .config import MULTI_TENANT_CONFIG, SELF_SERVICE_CONFIG
from .models import ApiListing, SubscriptionPlan, Tenant, TenantCreate
from .store import platform_store

router = APIRouter(prefix="/api/v1/platform", tags=["Platform (Level 2)"])


@router.get("/overview")
@require_permission("read")
async def get_level2_overview(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """Level 2 プラットフォーム概要"""
    return {
        "level": 2,
        "name": "Platform Level",
        "features": {
            "multi_tenant": {
                "tenants_count": len(platform_store.tenants),
                "isolation_mode": MULTI_TENANT_CONFIG["isolation_mode"],
            },
            "saas": {
                "plans_count": len(platform_store.plans),
                "self_service": SELF_SERVICE_CONFIG["enabled"],
            },
            "api_marketplace": {
                "listings_count": len(platform_store.api_listings),
            },
        },
    }


@router.get("/tenants", response_model=List[Tenant])
@require_permission("read")
async def list_tenants(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """テナント一覧"""
    return platform_store.list_tenants()


@router.post("/tenants", response_model=Tenant, status_code=status.HTTP_201_CREATED)
async def create_tenant(tenant: TenantCreate):
    """テナント作成（セルフサービスプロビジョニング）"""
    return platform_store.create_tenant(tenant.model_dump())


@router.get("/tenants/{tenant_id}", response_model=Tenant)
@require_permission("read")
async def get_tenant(
    tenant_id: str, current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """テナント詳細"""
    t = platform_store.get_tenant(tenant_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return t


@router.get("/plans", response_model=List[SubscriptionPlan])
@require_permission("read")
async def list_plans(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """サブスクリプションプラン一覧"""
    return platform_store.list_plans()


@router.get("/api-marketplace", response_model=List[ApiListing])
@require_permission("read")
async def list_api_marketplace(
    category: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """APIマーケットプレイス一覧"""
    return platform_store.list_api_listings(category=category)


@router.get("/self-service-config")
@require_permission("read")
async def get_self_service_config(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """セルフサービスプロビジョニング設定"""
    return SELF_SERVICE_CONFIG


@router.get("/multi-tenant-config")
@require_permission("read")
async def get_multi_tenant_config(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """マルチテナント設定"""
    return MULTI_TENANT_CONFIG
