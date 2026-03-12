# UEP v5.0 本番運用デプロイガイド

**更新**: 2026年3月

---

## 対象システム

| システム | フロントエンド | バックエンド | 本番用 .env |
|----------|----------------|--------------|-------------|
| **UEP v5.0** | ポート 3000 | ポート 8080 | `frontend/.env.production`, `backend/.env` |
| **産業統合プラットフォーム** | ポート 3010 | ポート 9010 | `industry_unified_platform/frontend/.env.production`, `backend/.env` |
| **企業横断オペレーション基盤（EOH）** | ポート 3020 | ポート 9020 | `enterprise_operations_hub/frontend/.env.production`, `enterprise_operations_hub/backend/.env` |

---

## 1. UEP v5.0 本番設定

### 1.1 環境変数

```bash
# バックエンド
cp backend/.env.production.example backend/.env
# SECRET_KEY, DATABASE_URL, CORS_ORIGINS を本番用に設定

# フロントエンド（ビルド時）
cp frontend/.env.production.example frontend/.env.production
# REACT_APP_API_URL, REACT_APP_INDUSTRY_UNIFIED_URL を本番ドメインに設定
```

| 変数 | 説明 | 本番例 |
|------|------|--------|
| `REACT_APP_API_URL` | UEP バックエンド API | `https://api.your-domain.com` |
| `REACT_APP_INDUSTRY_UNIFIED_URL` | 産業統合プラットフォームのURL | `https://industry.your-domain.com` |
| `REACT_APP_EOH_URL` | 企業横断オペレーション基盤（EOH）のURL | `https://eoh.your-domain.com` |

### 1.2 本番モード時の挙動

| 項目 | 本番時 |
|------|--------|
| **デモシード** | 無効 |
| **API ドキュメント** | /docs, /redoc 無効化 |
| **Chaos Engineering** | 無効化（403） |
| **SECRET_KEY** | デフォルト値では起動拒否 |

---

## 2. 産業統合プラットフォーム 本番設定

### 2.1 環境変数

```bash
# バックエンド（backend/.env に追記）
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=https://industry.your-domain.com,https://your-domain.com
INDUSTRY_UNIFIED_HOST=0.0.0.0
INDUSTRY_UNIFIED_PORT=9010

# フロントエンド（ビルド時）
cp industry_unified_platform/frontend/.env.production.example industry_unified_platform/frontend/.env.production
# REACT_APP_INDUSTRY_API_URL を本番APIドメインに設定
```

| 変数 | 説明 | 本番例 |
|------|------|--------|
| `REACT_APP_INDUSTRY_API_URL` | 産業統合バックエンド API | `https://api-industry.your-domain.com` |

### 2.2 本番モード時の挙動

| 項目 | 本番時 |
|------|--------|
| **デモシード** | 無効 |
| **API ドキュメント** | /docs, /redoc 無効化 |
| **CORS** | CORS_ORIGINS で指定したオリジンのみ許可 |
| **listen** | 0.0.0.0（全インターフェース） |

---

## 3. 企業横断オペレーション基盤（EOH）本番設定

### 3.1 環境変数

```bash
# バックエンド
cp enterprise_operations_hub/backend/.env.production.example enterprise_operations_hub/backend/.env
# EOH_SECRET_KEY, EOH_DATABASE_URL, EOH_CORS_ORIGINS を本番用に設定

# フロントエンド（ビルド時）
cp enterprise_operations_hub/frontend/.env.production.example enterprise_operations_hub/frontend/.env.production
# REACT_APP_EOH_API_URL を本番APIドメインに設定
```

| 変数 | 説明 | 本番例 |
|------|------|--------|
| `EOH_SECRET_KEY` | JWT署名用（必須） | `openssl rand -hex 32` で生成 |
| `EOH_DATABASE_URL` | PostgreSQL接続 | `postgresql://user:pass@host:5432/eoh_db` |
| `EOH_CORS_ORIGINS` | 許可オリジン | `https://eoh.your-domain.com` |
| `REACT_APP_EOH_API_URL` | EOH バックエンド API | `https://api-eoh.your-domain.com` |

### 3.2 本番モード時の挙動

| 項目 | 本番時 |
|------|--------|
| **デモシード** | 無効（サンプルデータ投入なし） |
| **API ドキュメント** | /docs, /redoc 無効化 |
| **SECRET_KEY** | デフォルト値では起動拒否 |
| **CORS** | EOH_CORS_ORIGINS で指定したオリジンのみ許可 |

---

## 4. デプロイ方法

### Docker Compose（UEP・産業統合）

```bash
export ENVIRONMENT=production
export DEBUG=false
export SECRET_KEY=$(openssl rand -hex 32)
docker-compose up -d
```

### 手動起動

```bash
# UEP バックエンド
cd backend && uvicorn main:app --host 0.0.0.0 --port 8080

# 産業統合バックエンド
cd industry_unified_platform && python main.py
# または ENVIRONMENT=production python main.py

# EOH バックエンド
cd enterprise_operations_hub/backend
ENVIRONMENT=production EOH_SECRET_KEY=$(openssl rand -hex 32) python -m uvicorn main:app --host 0.0.0.0 --port 9020

# フロントエンド（静的ビルドを nginx 等で配信）
cd frontend && npm run build
cd industry_unified_platform/frontend && npm run build
cd enterprise_operations_hub/frontend && npm run build
```

---

## 4. デプロイ前準備（必須作業）

### 4.1 環境変数・SECRET_KEY の準備

```bash
# Linux/macOS
chmod +x deploy/prepare-env.sh
./deploy/prepare-env.sh

# Windows PowerShell
.\deploy\prepare-env.ps1
```

`backend/.env` が作成され、SECRET_KEY が自動生成されます。DATABASE_URL、CORS_ORIGINS を本番用に編集してください。

### 4.2 HTTPS 化（nginx）

`deploy/nginx-ssl.conf.example` を参考に nginx を設定し、Let's Encrypt で証明書を取得します。

```bash
# 証明書取得例
certbot --nginx -d your-domain.com -d industry.your-domain.com -d eoh.your-domain.com -d api.your-domain.com -d api-industry.your-domain.com -d api-eoh.your-domain.com
```

### 4.3 本番ユーザー登録

**オプションA: 永続化あり（推奨）**

`backend/.env` に追加:
```
PRODUCTION_USERS_FILE=./data/production_users.json
```

バックエンド起動後、スクリプトで登録:
```bash
python scripts/register_production_user.py \
  --api-url https://api.your-domain.com \
  --username admin \
  --email admin@your-domain.com \
  --password "強力なパスワード" \
  --full-name "管理者"
```

**オプションB: API で登録**

```bash
curl -X POST https://api.your-domain.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","email":"admin@example.com","password":"強力なパスワード","full_name":"管理者"}'
```

※ PRODUCTION_USERS_FILE 未設定時は再起動でユーザーが消えます。

---

## 6. 本番前チェックリスト

### UEP
- [ ] `deploy/prepare-env.sh` または `prepare-env.ps1` を実行
- [ ] SECRET_KEY を本番用に生成・設定
- [ ] DATABASE_URL を PostgreSQL に設定
- [ ] CORS_ORIGINS にフロントエンドのドメインを指定
- [ ] REACT_APP_API_URL を本番APIのURLに設定
- [ ] REACT_APP_INDUSTRY_UNIFIED_URL を産業統合のURLに設定
- [ ] PRODUCTION_USERS_FILE を設定（本番ユーザー永続化）

### 産業統合
- [ ] CORS_ORIGINS に産業統合フロントのドメインを指定
- [ ] REACT_APP_INDUSTRY_API_URL を本番APIのURLに設定

### 企業横断オペレーション基盤（EOH）
- [ ] `enterprise_operations_hub/backend/.env.production.example` を `.env` にコピー
- [ ] EOH_SECRET_KEY を本番用に生成・設定（必須）
- [ ] EOH_DATABASE_URL を PostgreSQL に設定（推奨）
- [ ] EOH_CORS_ORIGINS に EOH フロントのドメインを指定
- [ ] REACT_APP_EOH_URL を本番 EOH のURLに設定（UEP フロント用）
- [ ] `enterprise_operations_hub/frontend/.env.production` に REACT_APP_EOH_API_URL を設定

### 共通
- [ ] 本番ユーザーを登録（scripts/register_production_user.py）
- [ ] ログレベルを WARNING 以上に設定
- [ ] HTTPS 化（deploy/nginx-ssl.conf.example を参考）

---

## 7. データ永続化について

現状、MLOps・インフラ構築・セキュリティセンター等のモジュールは **メモリ内ストア** を使用しています。本番運用でデータを永続化する場合は、各モジュールを PostgreSQL 等のデータベースに接続する改修が必要です。
