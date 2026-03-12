# 統合基盤 運用マニュアル

> 本システムは専門システムであり、デモ向きではない。UEP v5.0 は別のデモ用システム。

## 1. 起動・停止

### 起動

```bash
cd /mnt/c/uep-v5-ultimate-enterprise-platform/projects/unified-platform
chmod +x start.sh   # 初回のみ
./start.sh
```

### アクセス

- **URL**: http://localhost:8000
- **ログイン**: `kaho0525` / `0525`

### localhost が使えない場合（WSL）

```bash
hostname -I | awk '{print $1}'
```

表示された IP で `http://<IP>:8000` にアクセス。WSL 再起動で IP が変わる場合あり。

### ポート競合時

WSL 内に PostgreSQL/Redis がある場合、Docker 起動前に実行:

```bash
sudo service postgresql stop
sudo service redis-server stop
```

古いコンテナ: `docker compose down --remove-orphans` で削除。

### 停止

```bash
docker compose down
```

## 2. トラブルシューティング

| 状況 | 対処 |
|------|------|
| 接続拒否 | 1〜2分待って再試行。`docker compose logs app` でエラー確認 |
| ログインできない | `docker compose up -d --build` で再ビルド |
| 白い画面 | WSL IP でアクセス（`hostname -I`） |

## 3. ログ確認

```bash
docker compose logs -f app
```

## 4. シードデータ再投入

```bash
curl -X POST http://localhost:8000/api/v1/seed
```

またはブラウザで `http://localhost:8000/api/v1/seed` を開く。

## 5. DB バックアップ

```bash
docker compose exec db pg_dump -U unified unified > backup_$(date +%Y%m%d).sql
```

### バックアップ自動化（cron）

```bash
# 毎日 2:00 にバックアップ（WSL 内で crontab -e）
0 2 * * * cd /mnt/c/uep-v5-ultimate-enterprise-platform/projects/unified-platform && ./scripts/backup_db.sh ./backups
```
