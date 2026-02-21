"""
分散トレーシングモジュール
OpenTelemetryを使用したトレーシング
"""
import os
from typing import Any, Dict, Optional

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


class TracingHandler:
    """分散トレーシングハンドラークラス"""

    def __init__(self, service_name: str = "uep-backend"):
        """
        トレーシングハンドラーを初期化

        Args:
            service_name: サービス名
        """
        self.service_name = service_name
        self.tracer_provider: Optional[TracerProvider] = None
        self._initialize_tracer()

    def _initialize_tracer(self):
        """トレーサーを初期化"""
        try:
            # リソースを設定
            resource = Resource.create(
                {"service.name": self.service_name, "service.version": "5.0.0"}
            )

            # トレーサープロバイダーを作成
            self.tracer_provider = TracerProvider(resource=resource)

            # OTLPエクスポーターを設定（Jaeger等と互換）
            otlp_endpoint = os.getenv("OTLP_ENDPOINT", "http://localhost:4317")

            otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)

            # スパンプロセッサーを追加
            span_processor = BatchSpanProcessor(otlp_exporter)
            self.tracer_provider.add_span_processor(span_processor)

            # グローバルトレーサープロバイダーを設定
            trace.set_tracer_provider(self.tracer_provider)

        except Exception as e:
            # OpenTelemetryが利用できない場合は無視
            print(f"Failed to initialize tracing: {e}")
            self.tracer_provider = None

    def get_tracer(self, name: Optional[str] = None):
        """トレーサーを取得"""
        if self.tracer_provider:
            return trace.get_tracer(name or self.service_name)
        return None

    def start_span(self, name: str, attributes: Optional[Dict[str, Any]] = None):
        """スパンを開始"""
        tracer = self.get_tracer()
        if tracer:
            span = tracer.start_as_current_span(name)
            if attributes:
                for key, value in attributes.items():
                    span.set_attribute(key, str(value))
            return span
        return None


# グローバルインスタンス
tracing_handler = TracingHandler()
