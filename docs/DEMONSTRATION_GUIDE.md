# UEP v5.0 - デモンストレーションガイド

**作成日**: 2026 年 1 月 30 日  
**バージョン**: 5.0.0

---

## 概要

UEP v5.0（Ultimate Enterprise Platform v5.0）のデモンストレーション手順と起動方法を説明します。

---

## 前提条件

### 必要な環境

- **OS**: Windows 10/11
- **Python**: 3.11 以上
- **Node.js**: 18 以上
- **npm**: 9 以上

### 必要なソフトウェア

- Python 3.11+
- Node.js 18+
- Git（オプション）

---

## 起動方法

### 方法 1: バッチファイルを使用（推奨）

#### バックエンドの起動

```cmd
start-backend.bat
```

- 仮想環境の作成・有効化
- 依存関係のインストール
- バックエンドサーバーの起動（`http://localhost:8000`）

#### フロントエンドの起動

**別のコマンドプロンプトで実行:**

```cmd
start-frontend.bat
```

- 依存関係のインストール
- フロントエンドサーバーの起動（`http://localhost:3000`）

#### 一括起動

```cmd
start-all.bat
```

バックエンドとフロントエンドを順番に起動します。

### 方法 2: 手動で起動

#### バックエンド

```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### フロントエンド

```cmd
cd frontend
npm install
npm start
```

---

## デモンストレーション手順

### ステップ 1: システムの起動

1. **バックエンドを起動**

   ```cmd
   start-backend.bat
   ```

   - 起動確認: `http://localhost:8000/health` にアクセス
   - Swagger UI: `http://localhost:8000/docs` にアクセス

2. **フロントエンドを起動**（別のコマンドプロンプト）

   ```cmd
   start-frontend.bat
   ```

   - 起動確認: `http://localhost:3000` にアクセス

### ステップ 2: ログイン

1. ブラウザで `http://localhost:3000` にアクセス
2. ログイン画面で以下を入力:
   - **ユーザー名**: `kaho0525`
   - **パスワード**: `kaho052514`
3. 「ログイン」ボタンをクリック

### ステップ 3: 各機能の確認

#### ダッシュボード

- メインダッシュボードが表示される
- 各システムへのナビゲーションカードが表示される

#### MLOps

- パイプライン一覧
- モデル一覧
- 実験一覧

#### 生成 AI

- テキスト生成
- RAG クエリ
- CoT 推論

#### セキュリティコマンドセンター

- セキュリティイベント
- インシデント管理
- リスク分析

#### クラウドインフラ

- リソース管理
- IaC テンプレート
- デプロイメント管理

#### IDOP

- CI/CD パイプライン
- アプリケーション管理

#### AI 支援開発

- コード生成
- コードレビュー
- ドキュメント生成

#### 設定

- プロフィール設定
- セキュリティ設定
- 通知設定

---

## デモユーザー

| ユーザー名 | パスワード | ロール    | 権限     |
| ---------- | ---------- | --------- | -------- |
| kaho0525   | kaho052514 | admin     | 全権限   |
| developer  | dev123     | developer | 開発権限 |
| viewer     | view123    | viewer    | 閲覧権限 |

---

## API エンドポイント

### バックエンド API

- **ベース URL**: `http://localhost:8000`
- **API ドキュメント**: `http://localhost:8000/docs`
- **ヘルスチェック**: `http://localhost:8000/health`

### 主要な API エンドポイント

- `/api/v1/auth/*` - 認証・認可
- `/api/v1/mlops/*` - MLOps
- `/api/v1/generative-ai/*` - 生成 AI
- `/api/v1/security-center/*` - セキュリティコマンドセンター
- `/api/v1/cloud-infra/*` - クラウドインフラ
- `/api/v1/idop/*` - IDOP
- `/api/v1/ai-dev/*` - AI 支援開発

---

## トラブルシューティング

### よくある問題

#### 問題 1: バックエンドが起動しない

**症状**: `start-backend.bat`を実行してもエラーが発生

**解決方法**:

1. Python がインストールされているか確認: `python --version`
2. 仮想環境を再作成: `delete-venv.bat` → `rebuild-backend-simple.bat`
3. 依存関係を再インストール: `fix-backend.bat`

#### 問題 2: フロントエンドが起動しない

**症状**: `start-frontend.bat`を実行してもエラーが発生

**解決方法**:

1. Node.js がインストールされているか確認: `node --version`
2. 依存関係を再インストール:
   ```cmd
   cd frontend
   rmdir /s /q node_modules
   npm install
   ```

#### 問題 3: 422 エラーが発生する

**症状**: API リクエストが 422 エラーで失敗

**解決方法**:

1. バックエンドを再起動
2. 認証トークンが正しく設定されているか確認
3. 詳細は `docs/VALIDATION_ERROR_FIX.md` を参照

#### 問題 4: データが取得できない

**症状**: ページに「データの取得に失敗しました」と表示される

**解決方法**:

1. バックエンドが起動しているか確認: `http://localhost:8000/health`
2. ログインしているか確認
3. ブラウザのコンソールでエラーを確認
4. 詳細は `docs/API_ERROR_TROUBLESHOOTING.md` を参照

---

## 実装経緯

### プロジェクトの背景

UEP v5.0 は、企業が最重視する IT 戦略課題と需要が高いシステムを統合したエンタープライズプラットフォームです。

### 実装フェーズ

#### Phase 1: 統合基盤層の構築（1-2 ヶ月）

- ✅ Phase 1.1: 統合 API Gateway 構築
- ✅ Phase 1.2: 統合認証・認可システム構築
- ✅ Phase 1.3: 統合データレイク構築
- ✅ Phase 1.4: 統合イベントストリーミング構築
- ✅ Phase 1.5: 統合監視・オブザーバビリティ基盤構築
- ✅ Phase 1.6: 統合セキュリティ基盤構築

#### Phase 2: コアシステム層の統合（2-3 ヶ月）

- ✅ MLOps 基盤システム
- ✅ 生成 AI システム
- ✅ 監視・オブザーバビリティシステム
- ✅ 統合セキュリティコマンドセンター
- ✅ クラウドインフラシステム
- ✅ 統合開発・運用プラットフォーム（IDOP）
- ✅ AI 支援開発システム

#### Phase 3: 統合ダッシュボード層の構築（1-2 ヶ月）

- ✅ 統合管理ダッシュボード
- ✅ 統合セキュリティダッシュボード
- ✅ 統合 MLOps ダッシュボード

#### Phase 4: 統合テスト・最適化（1-2 ヶ月）

- ✅ 統合テスト
- ✅ パフォーマンス最適化
- ✅ セキュリティ強化

### 技術的な課題と解決

#### 課題 1: Windows 環境での実行

**問題**: 初期実装は WSL/Docker を前提としていた

**解決**: Windows ネイティブのバッチファイル（`.bat`）を作成し、直接実行可能に

**経緯**:

- Windows Command Prompt での文字化け問題 → `chcp 65001`で解決
- 仮想環境の削除・作成時の`Access is denied`エラー → `taskkill`と`attrib`コマンドで解決
- 依存関係のインストールエラー → リトライロジックと詳細なエラーメッセージで解決

#### 課題 2: 認証システムの実装

**問題**: OAuth2/OIDC、JWT、RBAC/ABAC の統合

**解決**:

- JWT 認証を実装
- RBAC デコレータを作成
- デモユーザーを実装

**経緯**:

- パスワードの 72 バイト制限 → bcrypt のバージョンを固定（4.0.1）して解決
- 認証情報の変更要求 → ユーザー名とパスワードを変更可能に

#### 課題 3: フロントエンドの実装

**問題**: React + TypeScript + Material-UI でのエンタープライズレベルの UI 実装

**解決**:

- Material-UI を使用したモダンな UI
- React Router によるルーティング
- 認証コンテキストによる状態管理

**経緯**:

- React.StrictMode による DOM 操作エラー → StrictMode を無効化して解決
- ログイン後のナビゲーションエラー → `replace: true`オプションと遅延処理で解決

#### 課題 4: API エラーハンドリング

**問題**: 422 バリデーションエラー、ネットワークエラーなどの適切な処理

**解決**:

- 詳細なエラーメッセージの表示
- バリデーションエラーの詳細表示
- ネットワークエラーの検出とメッセージ表示

**経緯**:

- `require_permission`デコレータが FastAPI の関数シグネチャを壊していた → `inspect.signature`と`functools.wraps`で解決
- CSP（Content Security Policy）が Swagger UI をブロック → `/docs`と`/redoc`パスで CSP を緩和

#### 課題 5: セキュリティ設定

**問題**: セキュリティヘッダーと CSP の適切な設定

**解決**:

- Swagger UI 用の CSP 緩和
- セキュリティヘッダーの適切な設定

**経緯**:

- Swagger UI のソースマップが CSP でブロックされる → `connect-src`に`cdn.jsdelivr.net`を追加

---

## よくある質問（FAQ）

### Q1: なぜ Windows 環境で実行するようにしたのですか？

**A**: デモンストレーション環境として、Windows デスクトップ PC での実行を想定していたためです。WSL や Docker Desktop が不要で、より簡単に起動できるようにしました。

### Q2: 認証情報は変更できますか？

**A**: はい、`backend/auth/routes.py`の`_init_demo_users`関数で変更できます。現在は`kaho0525` / `kaho052514`に設定されています。

### Q3: 本番環境での使用は可能ですか？

**A**: 現在の実装は開発・デモンストレーション用です。本番環境で使用する場合は、以下の点を確認・修正してください：

- セキュリティ設定の見直し
- データベースの設定（現在はメモリ内ストレージ）
- 環境変数の適切な設定
- ログとモニタリングの設定

### Q4: パフォーマンスはどの程度ですか？

**A**: 現在の実装は開発環境向けです。本番環境では、以下の最適化を推奨します：

- データベースの最適化
- キャッシング戦略の実装
- ロードバランシングの設定
- CDN の使用

---

## 参考資料

- [README.md](../README.md) - プロジェクト概要
- [QUICK_START_DESKTOP.md](QUICK_START_DESKTOP.md) - クイックスタートガイド
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - トラブルシューティング
- [API_ERROR_TROUBLESHOOTING.md](API_ERROR_TROUBLESHOOTING.md) - API エラー対処法
- [VALIDATION_ERROR_FIX.md](VALIDATION_ERROR_FIX.md) - バリデーションエラー対処法

---

以上
