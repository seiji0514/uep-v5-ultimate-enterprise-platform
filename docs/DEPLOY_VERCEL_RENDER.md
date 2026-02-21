# GitHub Actions + Vercel + Render デプロイ手順

UEP v5.0 を完全無料でクラウドデプロイする手順です。

## 構成

```
[GitHub]  main ブランチ push
    ├→ Vercel: フロントエンド (React)
    └→ Render: バックエンド API (FastAPI)
```

## 前提条件

- GitHub アカウント
- Vercel アカウント（https://vercel.com）
- Render アカウント（https://render.com）
- クレジットカード不要（無料枠内で運用）

---

## 0. GitHub にリポジトリを追加（未登録の場合）

リポジトリが GitHub にない場合、Render の一覧に表示されません。以下で追加してください。

### 方法A: スクリプト実行（推奨）

```powershell
# PowerShell で実行
cd c:\uep-v5-ultimate-enterprise-platform
.\scripts\add-to-github.ps1
```

### 方法B: 手動実行

```powershell
cd c:\uep-v5-ultimate-enterprise-platform
git init
git branch -M main
git add .
git commit -m "Initial commit: UEP v5.0"
```

### GitHub でリポジトリ作成

1. https://github.com/new を開く
2. リポジトリ名: **uep-v5-ultimate-enterprise-platform**
3. Public を選択
4. **README や .gitignore は追加しない**（既存コードを push するため）
5. Create repository をクリック

### push

```powershell
git remote add origin https://github.com/あなたのユーザー名/uep-v5-ultimate-enterprise-platform.git
git push -u origin main
```

完了後、Render でリポジトリ一覧を再読み込みすると表示されます。

---

## 1. Render の設定（バックエンド API）

### 1.1 新規 Web サービス作成

1. https://dashboard.render.com にログイン
2. **New** → **Web Service**
3. GitHub リポジトリを連携（初回のみ）

### 1.2 サービス設定

| 項目 | 値 |
|------|-----|
| **Name** | uep-backend |
| **Root Directory** | `backend` |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

### 1.3 環境変数（Render ダッシュボード → Environment）

| Key | Value |
|-----|-------|
| `ENVIRONMENT` | production |
| `DEBUG` | false |
| `RATE_LIMIT_ENABLED` | false |
| `SECRET_KEY` | （ランダムな文字列を生成） |

### 1.4 CORS 設定（デプロイ後に追加）

Vercel の URL が決まったら、以下を追加:

| Key | Value |
|-----|-------|
| `CORS_ORIGINS` | `https://your-app.vercel.app,https://uep-backend.onrender.com` |

### 1.5 Blueprint を使う場合（推奨）

1. **New** → **Blueprint**
2. リポジトリを選択
3. `render.yaml` が自動検出される
4. **Apply** でデプロイ

---

## 2. Vercel の設定（フロントエンド）

### 2.1 プロジェクト作成

1. https://vercel.com にログイン
2. **Add New** → **Project**
3. GitHub リポジトリを連携（初回のみ）

### 2.2 プロジェクト設定

| 項目 | 値 |
|------|-----|
| **Framework Preset** | Create React App |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` |
| **Output Directory** | `build` |

### 2.3 環境変数（Vercel ダッシュボード → Settings → Environment Variables）

| Key | Value |
|-----|-------|
| `REACT_APP_API_URL` | `https://uep-backend.onrender.com` |

※ Render の URL は `https://uep-backend.onrender.com`（サービス名により変更）

---

## 3. デプロイの流れ

1. **Render** を先にデプロイし、API の URL を確認
2. **Vercel** で `REACT_APP_API_URL` に Render の URL を設定
3. **Vercel** をデプロイ

以降、`main` ブランチへ push するたびに自動デプロイされます。

---

## 4. 無料枠の注意点

| サービス | 制限 |
|----------|------|
| **Render** | 15分でスリープ、再アクセス時に 50〜100 秒で起動 |
| **Vercel** | 100GB 帯域/月、無制限デプロイ |
| **GitHub Actions** | 月 2,000 分（パブリックリポは無制限） |

---

## 5. トラブルシューティング

### CORS エラー

- Render の `CORS_ORIGINS` に Vercel の URL を追加
- 末尾にスラッシュ不要、複数はカンマ区切り

### ログインできない

- Render のバックエンドが起動しているか確認（スリープ後は初回アクセスで遅延あり）
- 認証のデモユーザーは `backend/auth/routes.py` の `_init_demo_users` で定義

### ビルド失敗

- **Render**: `requirements.txt` の依存関係が重い場合、`requirements-render.txt` を用意して簡略化を検討
- **Vercel**: Node 18 以上推奨、`npm ci` で依存関係を固定

---

## 6. 職務経歴書での記載例

- **クラウドデプロイ**: GitHub Actions + Vercel + Render による CI/CD ・クラウドデプロイを構築
- **インフラ**: Vercel（フロント）、Render（API）での本番運用・監視を実施
