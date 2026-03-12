# Unified Platform 起動確認・最終チェック

## 実施日チェックリスト

### 1. ローカル（Python）起動確認

```bash
cd projects/unified-platform
set TESTING=true   # Windows
# export TESTING=true  # WSL/Linux

python -m pytest tests/ -v
# => 2 passed

python -c "from main import app; print('OK')"
# => OK
```

| 項目 | 結果 |
|------|------|
| pytest | ✅ 3 passed |
| main インポート | ✅ OK |
| 設定・ルート数 | ✅ 24 routes |

---

### 2. API エンドポイント確認（TESTING=true 時）

| エンドポイント | 期待 | 確認 |
|----------------|------|------|
| GET /health | 200 | ✅ |
| GET / | 200 | ✅ |
| GET /ready | 200 (DB接続時) | - |
| GET /metrics | 200 Prometheus | - |
| POST /api/v1/auth/login | 200 (admin/admin) | ✅ |

**ログイン確認例:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" -d "username=admin&password=admin"
# => {"access_token":"...","token_type":"bearer"}
```

---

### 3. Docker 起動確認（WSL 内で Docker Engine インストール後）

```bash
# WSL で
cd /mnt/c/uep-v5-ultimate-enterprise-platform/projects/unified-platform
docker compose config    # 構文チェック
docker compose up -d     # 起動
docker compose ps        # 状態確認
```

| サービス | ポート | 期待 |
|----------|--------|------|
| app | 8000 | running |
| db | 5432 | healthy |
| redis | 6379 | running |

**疎通確認:**
```bash
curl http://localhost:8000/health
curl http://localhost:8000/dashboard
```

---

### 4. 依存関係

```bash
pip install -r requirements.txt
pip check
# ※ 他プロジェクトのパッケージと競合する警告は unified-platform 単体では問題なし
```

---

### 5. ファイル構成

| パス | 用途 |
|------|------|
| main.py | 統合API |
| config.py | 設定 |
| database.py | DB接続 |
| models.py | テーブル定義 |
| seed_data.py | 初期データ |
| Dockerfile | イメージビルド |
| docker-compose.yml | オーケストレーション |
| k8s/ | K8s マニフェスト |
| .github/workflows/ | CI/CD |

---

### 6. 本番前の最終確認

- [ ] JWT_SECRET を本番用に変更
- [ ] DATABASE_URL を本番DBに設定
- [ ] REDIS_URL を本番Redisに設定
- [ ] 監査ログ有効（AUDIT_LOG_ENABLED=true）
- [ ] /docs の本番無効化検討
