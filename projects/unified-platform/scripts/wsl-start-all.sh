#!/bin/bash
# WSL: Docker 起動 + Unified Platform 一括起動
set -e
cd "$(dirname "$0")/.."

echo "[1/3] Docker 起動..."
sudo service docker start 2>/dev/null || true
sleep 2

echo "[2/3] Docker 疎通確認..."
until docker info >/dev/null 2>&1; do
  echo "  Docker 待機中..."
  sleep 2
done
echo "  Docker OK"

echo "[3/3] Unified Platform 起動..."
docker compose up -d --remove-orphans

echo ""
echo "起動完了（app の初回起動は seed 実行のため 10～20 秒かかることがあります）"
echo "  API:       http://localhost:8000"
echo "  Dashboard: http://localhost:8000/dashboard"
echo "  ログ:      docker compose logs -f app"
echo "  停止:      docker compose down"
