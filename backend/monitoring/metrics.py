"""
メトリクス収集モジュール
Prometheusメトリクスの収集と公開
"""
import time
from typing import Any, Dict

from fastapi import Response
from prometheus_client import (CONTENT_TYPE_LATEST, Counter, Gauge, Histogram,
                               generate_latest)


class MetricsCollector:
    """メトリクス収集クラス"""

    def __init__(self):
        """メトリクス収集器を初期化"""
        # HTTPリクエストメトリクス
        self.http_requests_total = Counter(
            "http_requests_total",
            "Total HTTP requests",
            ["method", "endpoint", "status"],
        )

        self.http_request_duration_seconds = Histogram(
            "http_request_duration_seconds",
            "HTTP request duration in seconds",
            ["method", "endpoint"],
        )

        # ビジネスメトリクス
        self.active_users = Gauge("active_users", "Number of active users")

        self.api_requests_total = Counter(
            "api_requests_total", "Total API requests", ["service", "endpoint"]
        )

        # エラーメトリクス
        self.errors_total = Counter(
            "errors_total", "Total errors", ["error_type", "service"]
        )

    def record_request(
        self, method: str, endpoint: str, status_code: int, duration: float
    ):
        """HTTPリクエストを記録"""
        self.http_requests_total.labels(
            method=method, endpoint=endpoint, status=str(status_code)
        ).inc()

        self.http_request_duration_seconds.labels(
            method=method, endpoint=endpoint
        ).observe(duration)

    def record_api_request(self, service: str, endpoint: str):
        """APIリクエストを記録"""
        self.api_requests_total.labels(service=service, endpoint=endpoint).inc()

    def record_error(self, error_type: str, service: str):
        """エラーを記録"""
        self.errors_total.labels(error_type=error_type, service=service).inc()

    def set_active_users(self, count: int):
        """アクティブユーザー数を設定"""
        self.active_users.set(count)

    def get_metrics(self) -> Response:
        """Prometheus形式のメトリクスを取得"""
        return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


# グローバルインスタンス
metrics_collector = MetricsCollector()
