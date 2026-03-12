#!/bin/bash
# WSL2 内で Kafka Streams を実行
# 前提: Kafka が docker compose up -d で起動済み
# 実行: wsl -e bash scripts/wsl-kafka-streams-run.sh
# または WSL ターミナルで: bash scripts/wsl-kafka-streams-run.sh

set -e

cd /mnt/c/uep-v5-ultimate-enterprise-platform/infrastructure/event-streaming/kafka-streams

# Java が無ければインストール
if ! command -v java &>/dev/null; then
    echo "Java が未インストールです。インストールします..."
    sudo apt update
    sudo apt install -y openjdk-17-jdk
fi

# gradlew の改行を修正
sed -i 's/\r$//' gradlew 2>/dev/null || true
chmod +x gradlew

# 前回の state を削除（ロック解除）
rm -rf build/kafka-streams-state

# Docker Desktop 使用時は localhost が届かない場合あり:
#   docker compose --profile event-streaming up -d kafka-streams  # Docker 内で実行（推奨）
# または KAFKA_BOOTSTRAP_SERVERS=$(grep nameserver /etc/resolv.conf|awk '{print $2}'):9092 を指定
echo "Kafka Streams を起動中..."
./gradlew run
