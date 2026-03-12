"""
分散トレーシングモジュール
OpenTelemetry + W3C Trace Context（traceparent, tracestate）
補強スキル: 分散トレーシング、サンプリング戦略、メトリクス連携
"""
import os
from typing import Any, Dict, Optional

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# サンプリング設定
SAMPLING_RATIO = float(os.getenv("OTEL_TRACES_SAMPLER_ARG", "1.0"))  # 1.0=100%, 0.1=10%
SAMPLING_STRATEGY = os.getenv("OTEL_TRACES_SAMPLER", "parentbased_traceidratio")


def _create_sampler():
    """サンプリング戦略を設定"""
    try:
        if SAMPLING_STRATEGY == "parentbased_traceidratio":
            from opentelemetry.sdk.trace.sampling import ParentBasedTraceIdRatioBased

            return ParentBasedTraceIdRatioBased(SAMPLING_RATIO)
        if SAMPLING_STRATEGY == "traceidratio":
            from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

            return TraceIdRatioBased(SAMPLING_RATIO)
        if SAMPLING_STRATEGY == "always_on":
            from opentelemetry.sdk.trace.sampling import AlwaysOn

            return AlwaysOn()
        if SAMPLING_STRATEGY == "always_off":
            from opentelemetry.sdk.trace.sampling import AlwaysOff

            return AlwaysOff()
    except Exception:
        pass
    return None


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

            # サンプリングを適用
            sampler = _create_sampler()
            self.tracer_provider = (
                TracerProvider(
                    resource=resource,
                    sampler=sampler,
                )
                if sampler
                else TracerProvider(resource=resource)
            )

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
        """スパンを開始（カスタムスパン）"""
        tracer = self.get_tracer()
        if tracer:
            span = tracer.start_as_current_span(name)
            if attributes:
                for key, value in attributes.items():
                    span.set_attribute(key, str(value))
            return span
        return None

    def span(self, name: str, attributes: Optional[Dict[str, Any]] = None):
        """コンテキストマネージャでカスタムスパン"""
        return _SpanContext(self, name, attributes or {})


class _SpanContext:
    """スパン用コンテキストマネージャ"""

    def __init__(
        self, handler: "TracingHandler", name: str, attributes: Dict[str, Any]
    ):
        self.handler = handler
        self.name = name
        self.attributes = attributes
        self.span = None

    def __enter__(self):
        self.span = self.handler.start_span(self.name, self.attributes)
        return self.span

    def __exit__(self, *args):
        if self.span:
            self.span.end()


# グローバルインスタンス
tracing_handler = TracingHandler()
