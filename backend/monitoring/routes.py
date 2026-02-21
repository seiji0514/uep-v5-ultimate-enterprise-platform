"""
監視APIエンドポイント
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from .metrics import metrics_collector
from .logging import logging_handler
from .tracing import tracing_handler
from auth.jwt_auth import get_current_active_user
import httpx
import os

router = APIRouter(prefix="/api/v1/monitoring", tags=["監視"])


@router.get("/metrics")
async def get_metrics(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """Prometheus形式のメトリクスを取得"""
    return metrics_collector.get_metrics()


@router.get("/health")
async def health_check():
    """ヘルスチェック（認証不要）"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "backend": "healthy",
            "prometheus": await _check_service("http://prometheus:9090/-/healthy"),
            "elasticsearch": await _check_service("http://elasticsearch:9200/_cluster/health"),
        }
    }


async def _check_service(url: str) -> str:
    """サービスのヘルスをチェック"""
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(url)
            if response.status_code == 200:
                return "healthy"
            return "unhealthy"
    except Exception:
        return "unreachable"


@router.get("/logs")
async def get_logs(
    service: Optional[str] = None,
    level: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    limit: int = 100,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """ログを取得（Elasticsearchから）"""
    try:
        elasticsearch_url = os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200")

        # クエリを構築
        query = {
            "size": limit,
            "sort": [{"timestamp": {"order": "desc"}}],
            "query": {
                "bool": {
                    "must": []
                }
            }
        }

        if service:
            query["query"]["bool"]["must"].append({
                "term": {"service": service}
            })

        if level:
            query["query"]["bool"]["must"].append({
                "term": {"log_level": level.upper()}
            })

        if start_time or end_time:
            time_range = {}
            if start_time:
                time_range["gte"] = start_time
            if end_time:
                time_range["lte"] = end_time
            query["query"]["bool"]["must"].append({
                "range": {"timestamp": time_range}
            })

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{elasticsearch_url}/uep-logs-*/_search",
                json=query
            )

            if response.status_code == 200:
                data = response.json()
                hits = data.get("hits", {}).get("hits", [])
                logs = [hit["_source"] for hit in hits]
                return {
                    "logs": logs,
                    "total": data.get("hits", {}).get("total", {}).get("value", 0),
                    "count": len(logs)
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to fetch logs from Elasticsearch"
                )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/traces")
async def get_traces(
    service: Optional[str] = None,
    trace_id: Optional[str] = None,
    limit: int = 100,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """トレースを取得"""
    # 実際の実装ではJaegerやZipkinから取得
    # ここでは簡易的な実装
    return {
        "message": "Tracing data retrieval not fully implemented",
        "service": service,
        "trace_id": trace_id
    }


@router.get("/stats")
async def get_stats(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """統計情報を取得"""
    return {
        "metrics": {
            "total_requests": "N/A",  # Prometheusから取得
            "active_users": "N/A",
            "error_rate": "N/A"
        },
        "services": {
            "backend": "running",
            "prometheus": await _check_service("http://prometheus:9090/-/healthy"),
            "elasticsearch": await _check_service("http://elasticsearch:9200/_cluster/health"),
            "kibana": await _check_service("http://kibana:5601/api/status"),
        },
        "timestamp": datetime.utcnow().isoformat()
    }
