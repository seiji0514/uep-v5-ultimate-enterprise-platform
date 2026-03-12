# UEP Standalone 障害対応 Runbook

## 1. サービス応答なし（AppDown）

**現象**: /health が応答しない

1. コンテナ状態確認: `docker compose ps`
2. アプリログ確認: `docker compose logs app --tail 100`
3. DB/Redis 状態: `docker compose ps db redis`
4. 再起動: `docker compose restart app`
5. 復旧しない場合: `docker compose down && docker compose up -d`

## 2. 高エラー率（HighErrorRate）

**現象**: 5xx が 5% 超

1. ログでエラー内容確認: `docker compose logs app | grep -E "5[0-9]{2}"`
2. DB 接続確認: `curl http://localhost:8000/ready`
3. リソース確認: `docker stats`
4. 必要に応じて app 再起動

## 3. 高レイテンシ（HighLatency）

**現象**: レスポンスが遅い

1. DB 負荷確認: `docker compose exec db psql -U unified -c "SELECT * FROM pg_stat_activity;"`
2. Redis 状態: `docker compose exec redis redis-cli INFO`
3. スロークエリ・接続数確認
4. 冗長構成の場合はインスタンス追加検討

## 4. DB 接続エラー

1. DB コンテナ: `docker compose ps db`
2. ヘルス: `docker compose exec db pg_isready -U unified`
3. 再起動: `docker compose restart db`
4. データ永続化確認: `docker volume ls`（pgdata）

## 5. ディスク容量不足

1. ログローテーション: 古いログ削除
2. Docker クリーン: `docker system prune -f`
3. Prometheus データ: `docker volume rm unified-platform_prometheus_data`（必要に応じて）
