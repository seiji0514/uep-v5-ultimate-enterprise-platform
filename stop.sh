#!/bin/bash
# UEP v5.0 - WSL環境での停止スクリプト

echo "=========================================="
echo "UEP v5.0 - サービス停止"
echo "=========================================="

# Docker Composeの確認
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "エラー: Docker Composeがインストールされていません"
    exit 1
fi

echo ""
echo "コンテナを停止・削除しています..."
docker-compose down -v || docker compose down -v

echo ""
echo "停止完了"
echo ""
