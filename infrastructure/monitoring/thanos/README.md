# Thanos（UEP v5.0）

補強スキル: Prometheus 長期保存、メトリクス履歴

## 概要

- Prometheus の長期ストレージ
- S3 互換オブジェクトストレージに保存
- 履歴クエリ対応

## デプロイ

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install thanos bitnami/thanos -f values.yaml
```
