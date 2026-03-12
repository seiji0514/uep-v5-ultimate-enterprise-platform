# HPA / VPA 設定（UEP v5.0）

補強スキル: Kubernetes オートスケーリング

## 構成

- `hpa-backend.yaml` - CPU/メモリベースの水平スケール
- `vpa-backend.yaml` - 垂直スケール（リソース推奨）

## 適用

```bash
kubectl apply -f hpa-backend.yaml
kubectl apply -f vpa-backend.yaml
```

## 前提

- metrics-server がクラスターにインストールされていること
- VPA は autoscaling.k8s.io の CRD が必要
