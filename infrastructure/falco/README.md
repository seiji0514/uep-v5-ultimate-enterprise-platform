# Falco 設定（UEP v5.0）

eBPF ベースのランタイムセキュリティ。カスタムルールで UEP 固有の異常を検知。

## 起動

```bash
docker-compose --profile security up -d falco
```

## Webhook 連携

Falco のアラートをバックエンドへ送信するには、`program_output` を設定:

```yaml
# falco.yaml
program_output:
  enabled: true
  program: "curl -s -X POST -H 'Content-Type: application/json' -d @- http://backend:8000/api/v1/security-defense-platform/falco/alerts"
```

受信エンドポイント: `POST /api/v1/security-defense-platform/falco/alerts`
