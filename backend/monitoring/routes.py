"""
監視APIエンドポイント
冗長化・フェイルオーバー・監視強化対応
"""
import os
import time
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status

from auth.jwt_auth import get_current_active_user
from core.health_failover import health_check_with_retry, service_health_registry

from .logging import logging_handler
from .metrics import metrics_collector
from .tracing import tracing_handler

router = APIRouter(prefix="/api/v1/monitoring", tags=["監視"])


async def _check_service_with_retry(url: str) -> Dict[str, Any]:
    """リトライ付きサービスヘルスチェック"""

    async def _check():
        try:
            start = time.perf_counter()
            async with httpx.AsyncClient(timeout=2.0) as client:
                r = await client.get(url)
                latency_ms = (time.perf_counter() - start) * 1000
                return {
                    "status": "healthy" if r.status_code == 200 else "unhealthy",
                    "latency_ms": latency_ms,
                }
        except Exception as e:
            return {"status": "unreachable", "error": str(e)}

    return await health_check_with_retry(_check, retries=2, timeout=3.0)


@router.get("/metrics")
async def get_metrics(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """Prometheus形式のメトリクスを取得"""
    return metrics_collector.get_metrics()


@router.get("/health")
async def health_check():
    """ヘルスチェック（認証不要・リトライ付き）"""

    async def _backend_check():
        return {"status": "healthy"}

    backend_result = await health_check_with_retry(_backend_check, retries=1)
    services = {
        "backend": backend_result.get("status", "healthy"),
    }
    # 外部サービスはオプション（失敗しても全体は healthy）
    try:
        prom_result = await _check_service("http://prometheus:9090/-/healthy")
        services["prometheus"] = (
            prom_result.get("result", {}).get("status", "unreachable")
            if prom_result.get("status") == "healthy"
            else "unreachable"
        )
    except Exception:
        services["prometheus"] = "unreachable"
    try:
        es_result = await _check_service("http://elasticsearch:9200/_cluster/health")
        services["elasticsearch"] = (
            es_result.get("result", {}).get("status", "unreachable")
            if es_result.get("status") == "healthy"
            else "unreachable"
        )
    except Exception:
        services["elasticsearch"] = "unreachable"

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": services,
        "retry_enabled": True,
    }


async def _check_service(url: str) -> Dict[str, Any]:
    """サービスのヘルスをチェック（リトライ付き）"""
    return await _check_service_with_retry(url)


@router.get("/health/detailed")
async def health_check_detailed():
    """詳細ヘルスチェック（監視強化・全サービス）"""
    all_status = service_health_registry.get_all_status()
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": all_status or {"backend": {"status": "healthy"}},
        "healthy_count": len(service_health_registry.get_healthy_services()),
    }


@router.get("/logs")
async def get_logs(
    service: Optional[str] = None,
    level: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    limit: int = 100,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """ログを取得（Elasticsearchから）"""
    try:
        elasticsearch_url = os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200")

        # クエリを構築
        query = {
            "size": limit,
            "sort": [{"timestamp": {"order": "desc"}}],
            "query": {"bool": {"must": []}},
        }

        if service:
            query["query"]["bool"]["must"].append({"term": {"service": service}})

        if level:
            query["query"]["bool"]["must"].append(
                {"term": {"log_level": level.upper()}}
            )

        if start_time or end_time:
            time_range = {}
            if start_time:
                time_range["gte"] = start_time
            if end_time:
                time_range["lte"] = end_time
            query["query"]["bool"]["must"].append({"range": {"timestamp": time_range}})

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{elasticsearch_url}/uep-logs-*/_search", json=query
            )

            if response.status_code == 200:
                data = response.json()
                hits = data.get("hits", {}).get("hits", [])
                logs = [hit["_source"] for hit in hits]
                return {
                    "logs": logs,
                    "total": data.get("hits", {}).get("total", {}).get("value", 0),
                    "count": len(logs),
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to fetch logs from Elasticsearch",
                )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/traces")
async def get_traces(
    service: Optional[str] = None,
    trace_id: Optional[str] = None,
    limit: int = 100,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """トレースを取得"""
    # 実際の実装ではJaegerやZipkinから取得
    # ここでは簡易的な実装
    return {
        "message": "Tracing data retrieval not fully implemented",
        "service": service,
        "trace_id": trace_id,
    }


@router.get("/stats")
async def get_stats(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """統計情報を取得"""
    return {
        "metrics": {
            "total_requests": "N/A",  # Prometheusから取得
            "active_users": "N/A",
            "error_rate": "N/A",
        },
        "services": {
            "backend": "running",
            "prometheus": await _check_service("http://prometheus:9090/-/healthy"),
            "elasticsearch": await _check_service(
                "http://elasticsearch:9200/_cluster/health"
            ),
            "kibana": await _check_service("http://kibana:5601/api/status"),
        },
        "timestamp": datetime.utcnow().isoformat(),
    }
