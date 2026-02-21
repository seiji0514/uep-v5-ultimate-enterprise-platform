"""
パフォーマンス最適化モジュール
"""
import time
from datetime import datetime
from functools import wraps
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class PerformanceMetrics(BaseModel):
    """パフォーマンスメトリクス"""

    endpoint: str
    avg_response_time: float
    p95_response_time: float
    p99_response_time: float
    request_count: int
    error_rate: float
    timestamp: datetime


class PerformanceOptimizer:
    """パフォーマンス最適化クラス"""

    def __init__(self):
        """パフォーマンス最適化器を初期化"""
        self._metrics: Dict[str, List[float]] = {}
        self._error_counts: Dict[str, int] = {}
        self._request_counts: Dict[str, int] = {}

    def record_request(
        self, endpoint: str, response_time: float, is_error: bool = False
    ):
        """リクエストを記録"""
        if endpoint not in self._metrics:
            self._metrics[endpoint] = []
            self._error_counts[endpoint] = 0
            self._request_counts[endpoint] = 0

        self._metrics[endpoint].append(response_time)
        self._request_counts[endpoint] += 1

        if is_error:
            self._error_counts[endpoint] += 1

        # メトリクスを保持（最新1000件）
        if len(self._metrics[endpoint]) > 1000:
            self._metrics[endpoint] = self._metrics[endpoint][-1000:]

    def get_metrics(self, endpoint: str) -> Optional[PerformanceMetrics]:
        """メトリクスを取得"""
        if endpoint not in self._metrics or not self._metrics[endpoint]:
            return None

        response_times = sorted(self._metrics[endpoint])
        request_count = self._request_counts.get(endpoint, 0)
        error_count = self._error_counts.get(endpoint, 0)

        avg = sum(response_times) / len(response_times)
        p95_index = int(len(response_times) * 0.95)
        p99_index = int(len(response_times) * 0.99)

        return PerformanceMetrics(
            endpoint=endpoint,
            avg_response_time=avg,
            p95_response_time=response_times[p95_index]
            if p95_index < len(response_times)
            else avg,
            p99_response_time=response_times[p99_index]
            if p99_index < len(response_times)
            else avg,
            request_count=request_count,
            error_rate=error_count / request_count if request_count > 0 else 0.0,
            timestamp=datetime.utcnow(),
        )

    def get_slow_endpoints(self, threshold: float = 1.0) -> List[Dict[str, Any]]:
        """遅いエンドポイントを取得"""
        slow_endpoints = []

        for endpoint, response_times in self._metrics.items():
            if response_times:
                avg_time = sum(response_times) / len(response_times)
                if avg_time > threshold:
                    slow_endpoints.append(
                        {
                            "endpoint": endpoint,
                            "avg_response_time": avg_time,
                            "request_count": self._request_counts.get(endpoint, 0),
                        }
                    )

        return sorted(
            slow_endpoints, key=lambda x: x["avg_response_time"], reverse=True
        )

    def optimize_endpoint(self, endpoint: str) -> Dict[str, Any]:
        """エンドポイントを最適化"""
        metrics = self.get_metrics(endpoint)
        if not metrics:
            return {"message": "No metrics available"}

        recommendations = []

        if metrics.avg_response_time > 1.0:
            recommendations.append("キャッシュの導入を検討")

        if metrics.error_rate > 0.05:
            recommendations.append("エラーハンドリングの改善を検討")

        if metrics.p99_response_time > 5.0:
            recommendations.append("データベースクエリの最適化を検討")

        return {
            "endpoint": endpoint,
            "current_metrics": metrics.dict(),
            "recommendations": recommendations,
        }


# グローバルインスタンス
performance_optimizer = PerformanceOptimizer()
