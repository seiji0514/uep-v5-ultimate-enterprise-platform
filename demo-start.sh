#!/bin/bash
# UEP v5.0 - デモンストレーション用起動スクリプト（デスクトップPC用）

echo "=========================================="
echo "UEP v5.0 - Ultimate Enterprise Platform"
echo "デモンストレーション用起動"
echo "=========================================="

# WSL環境の確認
if [ -z "$WSL_DISTRO_NAME" ] && [ -z "$WSLENV" ]; then
    echo "警告: WSL環境で実行されていない可能性があります"
    echo "このスクリプトはWSL環境で実行してください"
    exit 1
fi

# Dockerの確認
if ! command -v docker &> /dev/null; then
    echo "エラー: Dockerがインストールされていません"
    echo ""
    echo "WSL内でDockerをインストールする場合:"
    echo "  sudo ./install-docker-wsl.sh"
    echo ""
    echo "または、Docker Desktop for Windowsを使用する場合:"
    echo "  Docker Desktopをインストールし、WSL Integrationを有効化してください"
    exit 1
fi

# Docker Composeの確認
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "エラー: Docker Composeがインストールされていません"
    echo ""
    echo "インストール方法:"
    echo "  sudo apt-get install docker-compose-plugin"
    exit 1
fi

# Dockerサービスの確認
if ! systemctl is-active --quiet docker 2>/dev/null && ! docker ps &> /dev/null; then
    echo "警告: Dockerサービスが起動していない可能性があります"
    echo "Dockerサービスを起動してください:"
    echo "  sudo service docker start"
    echo "  または"
    echo "  sudo systemctl start docker"
    exit 1
fi

# ディレクトリの確認
if [ ! -f "docker-compose.yml" ]; then
    echo "エラー: docker-compose.ymlが見つかりません"
    echo "プロジェクトディレクトリに移動してください"
    exit 1
fi

echo ""
echo "デモンストレーション環境の準備..."
echo ""

# 既存のコンテナを停止・削除
echo "1. 既存のコンテナを停止・削除..."
docker-compose down -v 2>/dev/null || docker compose down -v 2>/dev/null

# イメージのビルド
echo ""
echo "2. イメージのビルド（初回は時間がかかります）..."
docker-compose build || docker compose build

# コンテナの起動
echo ""
echo "3. コンテナの起動..."
docker-compose up -d || docker compose up -d

# サービスの起動確認
echo ""
echo "4. サービスの起動確認（30秒待機）..."
sleep 30

echo ""
echo "=========================================="
echo "デモンストレーション環境の起動完了"
echo "=========================================="
echo ""
echo "📊 サービスURL:"
echo "  ✅ Backend API:        http://localhost:8000"
echo "  ✅ Kong Admin:         http://localhost:8001"
echo "  ✅ Kong Proxy:         http://localhost:8002"
echo "  ✅ Envoy Proxy:        http://localhost:8080"
echo "  ✅ Envoy Admin:        http://localhost:9901"
echo "  ✅ Prometheus:         http://localhost:9090"
echo "  ✅ Grafana:            http://localhost:3000"
echo "     (ユーザー名: admin / パスワード: admin)"
echo "  ✅ MinIO Console:      http://localhost:9001"
echo "     (ユーザー名: minioadmin / パスワード: minioadmin)"
echo ""
echo "🔍 ヘルスチェック:"
echo "  curl http://localhost:8000/health"
echo "  curl http://localhost:8002/api/v1/health"
echo "  curl http://localhost:8080/api/v1/health"
echo ""
echo "📝 ログ確認:"
echo "  docker-compose logs -f"
echo "  docker-compose logs -f backend"
echo ""
echo "🛑 停止:"
echo "  ./stop.sh"
echo "  または"
echo "  docker-compose down"
echo ""
echo "=========================================="
echo "デモンストレーション準備完了"
echo "=========================================="
echo ""
