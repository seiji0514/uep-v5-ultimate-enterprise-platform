#!/bin/bash
# UEP Standalone 統合起動スクリプト
# 用法: ./start.sh [モード...]
#   モード: default | monitoring | redundant
#   例: ./start.sh              → 通常起動
#       ./start.sh monitoring   → 監視付き
#       ./start.sh redundant    → 冗長構成
#       ./start.sh redundant monitoring → 冗長 + 監視

set -e
cd "$(dirname "$0")"

MONITORING=""
REDUNDANT=""

for arg in "$@"; do
  case "$arg" in
    monitoring) MONITORING=1 ;;
    redundant)  REDUNDANT=1 ;;
    default)    ;;
    *) echo "未知のモード: $arg (default|monitoring|redundant)"; exit 1 ;;
  esac
done

# バックエンド起動
if [ -n "$REDUNDANT" ]; then
  echo "冗長構成で起動..."
  COMPOSE_FILES="-f docker-compose.yml -f docker-compose.redundant.yml"
  PROFILES="--profile redundant"
else
  echo "通常起動..."
  COMPOSE_FILES="-f docker-compose.yml"
  PROFILES=""
fi

if [ -n "$MONITORING" ]; then
  echo "監視付き"
  PROFILES="$PROFILES --profile monitoring"
fi

# DEPLOY_MODE を export（docker compose が .env 経由で読む）
if [ -n "$REDUNDANT" ] && [ -n "$MONITORING" ]; then
  export DEPLOY_MODE="redundant+monitoring"
elif [ -n "$REDUNDANT" ]; then
  export DEPLOY_MODE="redundant"
elif [ -n "$MONITORING" ]; then
  export DEPLOY_MODE="monitoring"
else
  export DEPLOY_MODE="default"
fi

docker compose $COMPOSE_FILES down 2>/dev/null || true
docker compose $COMPOSE_FILES up -d --build $PROFILES
