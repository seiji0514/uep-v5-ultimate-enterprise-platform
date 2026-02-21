"""
最適化APIエンドポイント
"""
from typing import Any, Dict, List

from fastapi import APIRouter, Depends

from auth.jwt_auth import get_current_active_user
from auth.rbac import require_permission

from .caching import cache_manager
from .performance import performance_optimizer

router = APIRouter(prefix="/api/v1/optimization", tags=["最適化"])


@router.get("/performance/metrics")
@require_permission("read")
async def get_performance_metrics(
    endpoint: str, current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """パフォーマンスメトリクスを取得"""
    metrics = performance_optimizer.get_metrics(endpoint)
    if metrics:
        return metrics.dict()
    else:
        return {"message": "No metrics available for this endpoint"}


@router.get("/performance/slow-endpoints")
@require_permission("read")
async def get_slow_endpoints(
    threshold: float = 1.0,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """遅いエンドポイントを取得"""
    slow_endpoints = performance_optimizer.get_slow_endpoints(threshold=threshold)
    return {"slow_endpoints": slow_endpoints}


@router.post("/performance/optimize")
@require_permission("manage_infrastructure")
async def optimize_endpoint(
    endpoint: str, current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """エンドポイントを最適化"""
    result = performance_optimizer.optimize_endpoint(endpoint)
    return result


@router.get("/cache/stats")
@require_permission("read")
async def get_cache_stats(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """キャッシュ統計を取得"""
    return cache_manager.get_stats()


@router.delete("/cache/clear")
@require_permission("manage_infrastructure")
async def clear_cache(
    prefix: str = None, current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """キャッシュをクリア"""
    cache_manager.clear(prefix=prefix)
    return {"message": "Cache cleared"}
