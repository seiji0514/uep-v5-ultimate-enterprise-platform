#!/bin/bash
# WSL2 内で Docker をインストールするスクリプト
# 実行: wsl -e bash scripts/wsl-docker-setup.sh
# または WSL ターミナルで: bash scripts/wsl-docker-setup.sh

set -e

echo "=== 1. パッケージ更新 ==="
sudo apt update && sudo apt upgrade -y

echo "=== 2. 必要なパッケージ ==="
sudo apt install -y ca-certificates curl gnupg

echo "=== 3. Docker GPG キー ==="
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "=== 4. Docker リポジトリ追加 ==="
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "=== 5. Docker インストール ==="
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "=== 6. ユーザーを docker グループに追加 ==="
sudo usermod -aG docker $USER

echo "=== 7. Docker サービス起動 ==="
sudo service docker start

echo "=== 8. 動作確認 ==="
docker run --rm hello-world

echo "=== 9. Docker 自動起動を ~/.bashrc に追加 ==="
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/wsl-docker-autostart.sh" ]; then
    bash "$SCRIPT_DIR/wsl-docker-autostart.sh"
else
    # インラインで追加
    if ! grep -q "Docker auto-start (UEP)" "$HOME/.bashrc" 2>/dev/null; then
        echo '' >> "$HOME/.bashrc"
        echo '# Docker auto-start (UEP)' >> "$HOME/.bashrc"
        echo 'if service docker status 2>&1 | grep -q "is not running"; then' >> "$HOME/.bashrc"
        echo '    sudo service docker start 2>/dev/null' >> "$HOME/.bashrc"
        echo 'fi' >> "$HOME/.bashrc"
        echo "~/.bashrc に Docker 自動起動を追加しました"
    fi
fi

echo ""
echo "=== 完了 ==="
echo "WSL を一度 exit して再起動後、以下で Kafka を起動:"
echo "  cd /mnt/c/uep-v5-ultimate-enterprise-platform"
echo "  docker compose up -d zookeeper kafka"
