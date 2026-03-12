# Kyverno（UEP v5.0）

補強スキル: ポリシー as Code、ガバナンス

## 構成

- `policy-disallow-privileged.yaml` - 特権コンテナ禁止ポリシー

## 適用

```bash
kubectl apply -f policy-disallow-privileged.yaml
```

## 前提

- Kyverno がクラスターにインストールされていること
