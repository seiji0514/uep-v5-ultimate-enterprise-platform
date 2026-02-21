#!/bin/bash
# UEP v5.0 - WSL環境での再起動スクリプト

echo "=========================================="
echo "UEP v5.0 - サービス再起動"
echo "=========================================="

# 現在のディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 停止
./stop.sh

# 起動
./start.sh
