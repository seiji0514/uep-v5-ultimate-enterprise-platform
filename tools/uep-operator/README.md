# UEP Operator

UEP v5.0 Kubernetes Operator スケルトン
補強スキル: Go, Kubernetes Operator

## 概要

- controller-runtime ベースのスケルトン
- カスタムリソース（CRD）定義の拡張ポイント
- リコンサイルループの実装例

## ビルド

```bash
cd tools/uep-operator
go mod tidy
go build -o uep-operator .
```

## 拡張

1. `api/v1/` に CRD 型定義（例: UEPResource）
2. `controllers/` に Reconciler 実装
3. `main.go` で Manager 登録

## 参照

- [docs/UEP_v5_追加スキル・技術案.md](../../docs/UEP_v5_追加スキル・技術案.md)
- [ENHANCEMENTS.md](../../docs/ENHANCEMENTS.md)
