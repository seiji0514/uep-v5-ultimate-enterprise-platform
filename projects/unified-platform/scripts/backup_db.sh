#!/bin/bash
# Phase 4: DB バックアップスクリプト
# 使用方法: ./scripts/backup_db.sh [出力ディレクトリ]
# 例: ./scripts/backup_db.sh ./backups

OUT_DIR="${1:-./backups}"
mkdir -p "$OUT_DIR"
FILE="$OUT_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"
docker compose exec -T db pg_dump -U unified unified > "$FILE"
echo "Backup saved: $FILE"
