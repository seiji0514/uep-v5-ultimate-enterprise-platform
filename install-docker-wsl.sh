#!/bin/bash
# WSL内でDockerを直接インストールするスクリプト

set -e  # エラーが発生したら終了

echo "=========================================="
echo "WSL内でDockerをインストール"
echo "=========================================="

# 管理者権限の確認
if [ "$EUID" -ne 0 ]; then
    echo "このスクリプトはsudo権限が必要です"
    echo "実行方法: sudo ./install-docker-wsl.sh"
    exit 1
fi

# 現在のユーザーを取得
CURRENT_USER=${SUDO_USER:-$USER}

echo ""
echo "1. 既存のDockerパッケージを削除..."
apt-get remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true

echo ""
echo "2. 必要なパッケージをインストール..."
apt-get update
apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

echo ""
echo "3. Dockerの公式GPGキーを追加..."
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo ""
echo "4. Dockerリポジトリを追加..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

echo ""
echo "5. Dockerエンジンをインストール..."
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo ""
echo "6. systemdの設定確認..."
# systemdが使用可能か確認
if systemctl --version > /dev/null 2>&1; then
    echo "   systemdが使用可能です"
    # /etc/wsl.confの設定確認
    if [ ! -f /etc/wsl.conf ] || ! grep -q "systemd=true" /etc/wsl.conf 2>/dev/null; then
        echo "   /etc/wsl.confにsystemd設定を追加..."
        if [ ! -f /etc/wsl.conf ]; then
            touch /etc/wsl.conf
        fi
        if ! grep -q "^\[boot\]" /etc/wsl.conf 2>/dev/null; then
            echo "[boot]" >> /etc/wsl.conf
        fi
        if ! grep -q "^systemd=true" /etc/wsl.conf 2>/dev/null; then
            sed -i '/\[boot\]/a systemd=true' /etc/wsl.conf 2>/dev/null || echo "systemd=true" >> /etc/wsl.conf
        fi
        echo "   ⚠️  /etc/wsl.confを更新しました。WSL再起動が必要です。"
    fi
    echo "   Dockerサービスを起動..."
    systemctl enable docker 2>/dev/null || true
    systemctl start docker 2>/dev/null || true
else
    echo "   systemdが使用できません。手動起動モードを使用します。"
    echo "   ⚠️  Dockerサービスは手動で起動する必要があります:"
    echo "      sudo service docker start"
    echo "      または"
    echo "      sudo dockerd &"
fi

echo ""
echo "7. 現在のユーザーをdockerグループに追加..."
usermod -aG docker "$CURRENT_USER"
echo "   ユーザー $CURRENT_USER をdockerグループに追加しました"

echo ""
echo "8. Dockerサービスの起動確認..."
# systemdが使用できない場合の代替手段
if ! systemctl is-active --quiet docker 2>/dev/null; then
    echo "   systemd経由で起動できないため、手動で起動を試みます..."
    service docker start 2>/dev/null || dockerd > /dev/null 2>&1 &
    sleep 2
fi

# Dockerが動作しているか確認
if docker ps > /dev/null 2>&1; then
    echo "   ✅ Dockerは動作しています"
else
    echo "   ⚠️  Dockerサービスが起動していません"
    echo "   手動で起動してください: sudo service docker start"
fi

echo ""
echo "=========================================="
echo "Dockerのインストールが完了しました"
echo "=========================================="
echo ""
echo "次のステップ:"
echo ""
echo "1. WSLを再起動してください（重要）:"
echo "   exit"
echo "   # Windows側のPowerShellまたはコマンドプロンプトで:"
echo "   wsl --shutdown"
echo "   # その後、再度WSL（Ubuntu）を起動"
echo ""
echo "2. WSL再起動後、Dockerが動作するか確認:"
echo "   docker --version"
echo "   docker compose version"
echo "   docker ps"
echo ""
echo "3. Dockerサービスが起動していない場合:"
echo "   sudo service docker start"
echo ""
echo "4. デモンストレーションを起動:"
echo "   cd /mnt/c/uep-v5-ultimate-enterprise-platform"
echo "   ./demo-start.sh"
echo ""
