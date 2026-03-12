# クイックスタートガイド

## 【システム概要】

スマートシティ×サステナビリティ統合プラットフォーム（統合版）のMVP（Minimum Viable Product）です。

## 【前提条件】

### オプション1: Docker使用（推奨）
- **Docker Desktop**（またはDocker + Docker Compose）がインストールされていること
- **サーバー不要**: ローカルPC（Windows、Mac、Linux）で実行可能

### オプション2: Docker不使用
- **Python 3.13**（または3.11以上）
- **Node.js 20**（または18以上）
- **PostgreSQL**（またはSQLite使用で不要）

詳細は以下を参照してください：
- Docker使用: `LOCAL_DEVELOPMENT.md`
- Docker不使用: `SETUP_WITHOUT_DOCKER.md`

## 【セットアップ手順】

### 1. 環境変数の設定

```bash
cd smart-city-sustainability-platform
cp .env.example .env
# .envファイルを編集して環境変数を設定
```

### 2. Docker Composeで起動

```bash
docker-compose up -d
```

### 3. データベースマイグレーション（初回のみ）

```bash
docker-compose exec backend alembic upgrade head
```

### 4. アクセス

**外部からのアクセス（ブラウザ等）:**
- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:8000
- **APIドキュメント**: http://localhost:8000/docs
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090

**コンテナ間通信（内部）:**
- バックエンド → PostgreSQL: `postgres:5432`
- バックエンド → InfluxDB: `http://influxdb:8086`
- バックエンド → Kafka: `kafka:9092`
- フロントエンド → バックエンド: `http://backend:8000`（Viteプロキシ経由）

## 【主要機能】

### 1. IoTセンサー統合監視
- 環境データ（大気、水質、土壌、生物多様性）
- 交通データ（交通量、渋滞、事故）
- エネルギーデータ（電力、ガス、再生可能エネルギー）
- セキュリティデータ（防犯、災害、緊急事態）
- インフラデータ（橋梁、道路、建物、設備）

### 2. 環境管理・サステナビリティ機能
- 環境データ分析・予測
- ESGレポート自動生成
- カーボンフットプリント管理・可視化
- 環境リスク評価・アラート

### 3. スマートシティ管理機能
- 統括責任者向け統合ダッシュボード
- データ分析・予測
- 自動制御・最適化
- 災害対応統合
- アクセシビリティ情報統合

### 4. 統括責任者向け判断支援
- 環境管理とスマートシティ管理の統合判断支援
- 災害対応統括経験を基にした判断支援システム
- 複数データソースの統合分析
- シナリオ分析・最悪ケース予測
- 自動Runbook生成

### 5. レポート・可視化機能
- ESGレポート自動生成
- スマートシティ統合レポート
- 環境データ可視化
- リアルタイムダッシュボード
- カスタムレポート生成

## 【APIエンドポイント例】

### IoTセンサー
- `GET /api/v1/sensors/` - センサー一覧
- `POST /api/v1/sensors/` - センサー作成
- `GET /api/v1/sensors/{sensor_id}` - センサー詳細

### 環境データ
- `GET /api/v1/environment/data` - 環境データ取得
- `POST /api/v1/environment/data` - 環境データ作成
- `GET /api/v1/environment/analysis` - 環境データ分析
- `GET /api/v1/environment/predictions` - 環境データ予測

### ESGレポート
- `GET /api/v1/esg/reports` - ESGレポート一覧
- `POST /api/v1/esg/reports/generate` - ESGレポート自動生成
- `GET /api/v1/esg/carbon-footprint` - カーボンフットプリント取得

### ダッシュボード
- `GET /api/v1/dashboard/overview` - ダッシュボード概要
- `GET /api/v1/dashboard/kpi` - 統合KPI
- `GET /api/v1/dashboard/alerts-summary` - アラートサマリー

## 【開発環境での実行】

### バックエンド
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### フロントエンド
```bash
cd frontend
npm install
npm start
```

## 【次のステップ】

1. **データ投入**: サンプルデータの投入
2. **機能拡張**: 各機能の詳細実装
3. **テスト**: ユニットテスト、統合テストの追加
4. **本番環境**: 本番環境へのデプロイメント準備

---

**ご質問・ご要望がございましたら、お気軽にお申し付けください。**

