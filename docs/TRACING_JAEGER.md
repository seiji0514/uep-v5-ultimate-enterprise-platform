# 分散トレーシング（OpenTelemetry + Jaeger）

補強スキル: 分散トレーシング、W3C Trace Context

## 概要

- **OpenTelemetry SDK**: トレース・スパン収集
- **Jaeger**: トレース可視化（OTLP gRPC 4317）
- **W3C Trace Context**: `traceparent`, `tracestate` ヘッダーでトレースID伝搬

## 起動

```bash
docker-compose up -d jaeger backend
```

## Jaeger UI

- URL: http://localhost:16686
- Service: `uep-backend` で検索

## カスタムスパン

重要処理に手動スパンを追加:

```python
from monitoring.tracing import tracing_handler

with tracing_handler.span("my_operation", {"key": "value"}):
    # 処理
    pass
```

## トレース伝搬

クライアントが `traceparent` ヘッダーを送ると、同じトレースに紐づく。
例: `traceparent: 00-<trace_id>-<span_id>-01`
