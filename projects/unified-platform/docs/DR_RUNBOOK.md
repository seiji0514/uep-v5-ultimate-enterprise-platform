# Phase 4: Disaster Recovery Runbook

## RTO/RPO 目標
- RTO: 4時間以内
- RPO: 1時間以内（DBバックアップ間隔）

## フェイルオーバー手順

### 1. プライマリ障害検知
- ヘルスチェック失敗（/health, /ready）
- Prometheus アラート: ProbeDown, HighErrorRate

### 2. DRサイト切替
```bash
# Ingress/Route を DR サイトへ切替
kubectl patch ingress unified-platform -p '{"spec":{"rules":[{"host":"dr.example.com"}]}}'

# または Blue-Green で Green (DR) を有効化
./scripts/blue-green-switch.sh green
```

### 3. DB レプリカ昇格
```bash
# PostgreSQL スタンバイをプライマリに昇格
pg_ctl promote -D /var/lib/postgresql/data
```

### 4. 復旧確認
- /health, /ready 確認
- 主要API 疎通確認
- 監査ログ整合性確認

## バックアップ
- PostgreSQL: 日次フル + 1時間WALアーカイブ
- Redis: RDB スナップショット 6時間毎
- 設定・シークレット: Git管理
