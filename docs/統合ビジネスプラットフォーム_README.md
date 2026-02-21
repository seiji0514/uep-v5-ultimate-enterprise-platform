# 統合ビジネスプラットフォーム

**作成日**: 2026年2月  
**バージョン**: 1.0.0  
**難易度**: ⭐⭐⭐⭐⭐ 実用的最高難易度

---

## 概要

業務効率化・DX / 人材・組織 / 顧客対応・CX の3システムを1つの統合プラットフォームにまとめたシステムです。  
UEP v5.0 の **8番目コアシステム** として組み込まれています。

### 実用的最高難易度の実装

| 項目 | 内容 |
|------|------|
| 多段階承認 | 金額に応じた条件分岐（10万円未満: 1段階、10万円以上: 2段階、100万円以上: 3段階） |
| イベント駆動 | Kafka統合（workflow, approval, tickets トピック） |
| Prometheusメトリクス | 全モジュールの操作をメトリクス化 |
| 監査ログ | 全操作を記録、`GET /api/v1/unified-business/audit-logs` で取得 |

---

## 統合モジュール

### 1. 業務効率化・DX

| 機能 | 説明 | API |
|------|------|-----|
| ワークフロー自動化 | ワークフローの作成・管理 | `POST /api/v1/unified-business/workflows` |
| 申請・承認フロー | 申請の作成・承認/却下 | `POST /api/v1/unified-business/approval-requests` |
| RPA | RPAジョブの作成・実行 | `POST /api/v1/unified-business/rpa/jobs` |

### 2. 人材・組織

| 機能 | 説明 | API |
|------|------|-----|
| 障害者雇用支援 | 配慮事項の登録・チェックリスト | `POST /api/v1/unified-business/hr/disability-supports` |
| オンボーディング | タスク作成・テンプレート一括作成 | `POST /api/v1/unified-business/hr/onboarding/tasks` |
| スキルマッチング | 社員スキル登録・マッチング検索 | `POST /api/v1/unified-business/hr/skill-matching/find` |

### 3. 顧客対応・CX

| 機能 | 説明 | API |
|------|------|-----|
| チケット管理 | 問い合わせチケットの作成・ステータス更新 | `POST /api/v1/unified-business/customer/tickets` |
| AIチャットボット | FAQ応答（ルールベース） | `POST /api/v1/unified-business/customer/chat` |
| 監査ログ | セキュリティ・コンプライアンス用ログ取得 | `GET /api/v1/unified-business/audit-logs` |

---

## ディレクトリ構成

```
backend/unified_business_platform/
├── __init__.py
├── models.py          # Pydanticモデル
├── workflow.py        # 業務効率化・DX（多段階承認・条件分岐）
├── hr.py              # 人材・組織（障害者雇用、オンボーディング、スキルマッチング）
├── customer_support.py # 顧客対応・CX（チケット、チャットボット）
├── routes.py          # APIエンドポイント（メトリクス・監査・イベント統合）
├── metrics.py         # Prometheusメトリクス
├── audit.py           # 監査ログ
└── events.py          # Kafkaイベント発行

frontend/src/
├── api/unifiedBusiness.ts
└── components/UnifiedBusiness/UnifiedBusinessPage.tsx
```

---

## アクセス方法

1. UEP v5.0 にログイン（kaho0525 / kaho052514 または developer / dev123）
2. サイドメニューから「統合ビジネスプラットフォーム」を選択
3. または `/unified-business` に直接アクセス

---

## API 認証

全エンドポイントは JWT 認証が必要です。`/api/v1/auth/login` でトークンを取得し、`Authorization: Bearer <token>` でリクエストしてください。

---

以上
