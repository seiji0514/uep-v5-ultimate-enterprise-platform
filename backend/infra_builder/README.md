# インフラ構築専用システム (Infra Builder)

**UEP v5.0 統合モジュール**  
インフラ構築に特化したワークフロー管理システム。

---

## 概要

設計 → 構築 → デプロイ → 検証の一連の流れを管理する専用システム。  
Docker、Kubernetes、Terraform に対応。UEP v5.0 に統合済み。

---

## 機能

| 機能 | 説明 |
|------|------|
| **構築プロジェクト** | インフラ構築プロジェクトの作成・管理 |
| **ブループリント** | IaC テンプレート（Terraform、Docker Compose、K8s）の管理 |
| **パイプライン実行** | 設計→構築→デプロイ→検証のワークフロー実行 |
| **ダッシュボード** | プロジェクト数、進行状況、ブループリント数のサマリー |

---

## API エンドポイント

| メソッド | パス | 説明 |
|----------|------|------|
| GET | `/api/v1/infra-builder/dashboard` | ダッシュボードサマリー |
| GET | `/api/v1/infra-builder/projects` | プロジェクト一覧 |
| POST | `/api/v1/infra-builder/projects` | プロジェクト作成 |
| GET | `/api/v1/infra-builder/projects/{id}` | プロジェクト取得 |
| GET | `/api/v1/infra-builder/blueprints` | ブループリント一覧 |
| POST | `/api/v1/infra-builder/blueprints` | ブループリント作成 |
| GET | `/api/v1/infra-builder/pipelines` | パイプライン実行一覧 |
| POST | `/api/v1/infra-builder/pipelines/run` | パイプライン実行 |

---

## フロントエンド

- **パス**: `/infra-builder`
- **コンポーネント**: `InfraBuilderPage.tsx`
- **メニュー**: サイドバー「インフラ構築専用」

---

## 技術スタック

- **バックエンド**: FastAPI, Pydantic
- **認証**: JWT, RBAC (`require_permission`, `manage_infrastructure`)
- **フロントエンド**: React, TypeScript, Material-UI

---

## デモデータ

起動時に以下のサンプルデータが自動投入されます：

- プロジェクト: Webアプリ基盤構築、Kubernetes クラスタ構築
- ブループリント: Docker Compose 基本構成、Terraform AWS VPC
- パイプライン実行: 1件の成功履歴
