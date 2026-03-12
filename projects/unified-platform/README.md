# Unified Platform: Medical + Aviation + Space

医療・航空・宇宙を1つに統合した高難度・実用的な大規模運用システム。UEP v5.0 本体から切り離したスタンドアロン版。**API + React フロントエンド**。

## Phase 実装状況

| Phase | 内容 | 状態 |
|-------|------|------|
| **1** | DB導入、Docker化 | ✅ PostgreSQL, Docker, docker-compose |
| **2** | Redis、認証、監査ログ | ✅ JWT, API Key, AuditLog, Redis |
| **3** | Kubernetes、HPA、監視 | ✅ K8s, HPA, Prometheus, /health, /ready, /metrics |
| **4** | CI/CD、Blue-Green、DR | ✅ GitHub Actions, Blue-Green manifests, DR Runbook |
| **5** | 分散トレーシング、コンプライアンス | ✅ OpenTelemetry準備, AuditLog, Prometheus |

## クイックスタート

### WSL 一括起動（Docker Engine が WSL 内にある場合）

```bash
cd projects/unified-platform
bash scripts/wsl-start-all.sh
```
→ Docker 起動 + app/db/redis 一括起動

### Docker Compose（手動）

```bash
cd projects/unified-platform
docker compose up -d
```

- **アプリ**: http://localhost:8000（本番・ビルド済みフロント）
- API 一覧（簡易）: http://localhost:8000/dashboard
- Swagger: http://localhost:8000/docs
- **ログイン**: kaho0525 / 0525

### ローカル（DB・Redis 別途起動）

```bash
# PostgreSQL, Redis を起動後
pip install -r requirements.txt
python seed_data.py
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 監視付き起動

```bash
docker compose --profile monitoring up -d
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)
```

## API 概要

| ドメイン | エンドポイント例 |
|----------|------------------|
| Medical | /api/v1/medical/ai-diagnosis, /vital-signs, /fhir/patient/{id} |
| Aviation | /api/v1/aviation/flights, /airports, /delays |
| Space | /api/v1/space/satellites, /launches, /apod |
| Unified | /api/v1/unified/stats |
| Auth | POST /api/v1/auth/login (admin/admin), X-API-Key: unified-demo-key |

## Kubernetes

```bash
# デプロイ
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/hpa.yaml

# Blue-Green
kubectl apply -f k8s/blue-green/deployment-blue.yaml
kubectl apply -f k8s/blue-green/deployment-green.yaml
```

## 環境変数

| 変数 | 説明 |
|------|------|
| DATABASE_URL | PostgreSQL (async) |
| REDIS_URL | Redis |
| JWT_SECRET | JWT署名用 |
| AUDIT_LOG_ENABLED | 監査ログ有効化 |
| OTLP_ENDPOINT | OpenTelemetry (Phase 5) |
