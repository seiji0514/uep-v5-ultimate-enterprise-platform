# Crossplane（UEP v5.0）

補強スキル: IaC、クラウドリソースの Kubernetes 管理

## 概要

- クラウドリソース（RDS, S3 等）を Kubernetes リソースとして管理
- GitOps と連携可能

## セットアップ

```bash
helm install crossplane crossplane-stable/crossplane -n crossplane-system --create-namespace
kubectl apply -f provider-config.yaml
```
