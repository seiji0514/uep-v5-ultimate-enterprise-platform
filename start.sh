#!/bin/bash
# UEP v5.0 - WSL環境での起動スクリプト

echo "=========================================="
echo "UEP v5.0 - Ultimate Enterprise Platform"
echo "WSL環境での起動"
echo "=========================================="

# WSL環境の確認
if [ -z "$WSL_DISTRO_NAME" ] && [ -z "$WSLENV" ]; then
    echo "警告: WSL環境で実行されていない可能性があります"
fi

# Dockerの確認
if ! command -v docker &> /dev/null; then
    echo "エラー: Dockerがインストールされていません"
    echo "Docker Desktop for Windowsをインストールするか、WSL内でDockerをインストールしてください"
    exit 1
fi

# Docker Composeの確認
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "エラー: Docker Composeがインストールされていません"
    exit 1
fi

# ディレクトリの確認
if [ ! -f "docker-compose.yml" ]; then
    echo "エラー: docker-compose.ymlが見つかりません"
    exit 1
fi

echo ""
echo "1. 既存のコンテナを停止・削除..."
docker-compose down -v 2>/dev/null || docker compose down -v 2>/dev/null

echo ""
echo "2. イメージのビルド..."
docker-compose build --no-cache || docker compose build --no-cache

echo ""
echo "3. コンテナの起動..."
docker-compose up -d || docker compose up -d

echo ""
echo "4. サービスの起動確認..."
sleep 5

echo ""
echo "=========================================="
echo "起動完了"
echo "=========================================="
echo ""
echo "サービスURL:"
echo "  - Backend API: http://localhost:8000"
echo "  - Kong Admin: http://localhost:8001"
echo "  - Kong Proxy: http://localhost:8002"
echo "  - Envoy Proxy: http://localhost:8080"
echo "  - Envoy Admin: http://localhost:9901"
echo "  - Prometheus: http://localhost:9090"
echo "  - Grafana: http://localhost:3000 (admin/admin)"
echo "  - MinIO Console: http://localhost:9001 (minioadmin/minioadmin)"
echo ""
echo "ヘルスチェック:"
echo "  curl http://localhost:8000/health"
echo "  curl http://localhost:8002/api/v1/health"
echo "  curl http://localhost:8080/api/v1/health"
echo ""
echo "ログ確認:"
echo "  docker-compose logs -f"
echo ""
echo "停止:"
echo "  docker-compose down"
echo ""
