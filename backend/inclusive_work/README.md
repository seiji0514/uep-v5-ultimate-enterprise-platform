# インクルーシブ雇用AIプラットフォーム

障害者雇用マッチング + アクセシビリティ特化AI + AIエージェント基盤 + 当事者視点UX評価を統合したプラットフォーム。

## 機能

| 機能 | エンドポイント | 説明 |
|------|----------------|------|
| マッチング | POST /api/v1/inclusive-work/matching | スキル・勤務形態で求人マッチング |
| アクセシビリティAI | POST /api/v1/inclusive-work/chat | 音声・簡易UI対応チャット |
| UX評価 | POST /api/v1/inclusive-work/ux-evaluation | 企業サイトのアクセシビリティ評価 |
| AIエージェント | POST /api/v1/inclusive-work/agent | マッチング・相談・評価エージェント |

## 起動

UEP v5.0 バックエンドに統合済み。バックエンド起動時に自動で有効化されます。

```
cd backend
python -m uvicorn main:app --reload
```

フロントエンド: サイドメニュー「インクルーシブ雇用AI」からアクセス。

## 将来のUEP統合

本モジュールは UEP v5.0 とは別コンセプトで開発。後から UEP に組み込む形で統合済み。
