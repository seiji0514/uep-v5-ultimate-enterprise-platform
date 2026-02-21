# WSL内でDockerを直接インストールする手順

**作成日**: 2026年1月29日  
**対象**: Docker Desktop for Windowsが使用できない環境（ノートPC等）

---

## 📋 前提条件

- WSL2がインストールされていること
- Ubuntu/DebianベースのWSLディストリビューションを使用していること
- 管理者権限（sudo）が使用できること

---

## 🚀 インストール手順

### 方法1: 自動インストールスクリプトを使用（推奨）

```bash
# プロジェクトディレクトリに移動
cd ~/uep-v5-ultimate-enterprise-platform
# または
cd /mnt/d/AI_system_research/開発プロジェクト/AI\ system\ research\ and\ development\ track\ record/uep-v5-ultimate-enterprise-platform

# 実行権限を付与
chmod +x install-docker-wsl.sh

# インストール実行（sudo権限が必要）
sudo ./install-docker-wsl.sh
```

### 方法2: 手動インストール

```bash
# 1. 既存のDockerパッケージを削除
sudo apt-get remove -y docker docker-engine docker.io containerd runc

# 2. 必要なパッケージをインストール
sudo apt-get update
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 3. Dockerの公式GPGキーを追加
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 4. Dockerリポジトリを追加
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Dockerエンジンをインストール
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 6. Dockerサービスを起動
sudo systemctl enable docker
sudo systemctl start docker

# 7. 現在のユーザーをdockerグループに追加
sudo usermod -aG docker $USER
```

---

## 🔄 WSLの再起動

インストール後、WSLを再起動する必要があります：

```bash
# WSL内で
exit

# Windows側のPowerShellまたはコマンドプロンプトで
wsl --shutdown

# 再度WSLを起動
```

---

## ✅ インストール確認

WSLを再起動後、以下で確認：

```bash
# Dockerのバージョン確認
docker --version

# Docker Composeのバージョン確認
docker compose version

# Dockerサービスの状態確認
sudo systemctl status docker

# テスト実行（sudo不要になるはず）
docker run hello-world
```

---

## 🚨 トラブルシューティング

### Dockerサービスが起動しない

```bash
# サービスの状態確認
sudo systemctl status docker

# サービスを起動
sudo systemctl start docker

# サービスを有効化（自動起動）
sudo systemctl enable docker
```

### systemdが使用できない場合

WSL2では、systemdがデフォルトで無効になっている場合があります。

**解決方法1**: `/etc/wsl.conf`を編集

```bash
sudo nano /etc/wsl.conf
```

以下を追加：

```ini
[boot]
systemd=true
```

WSLを再起動：

```powershell
# Windows側で
wsl --shutdown
```

**解決方法2**: Dockerサービスを手動で起動

```bash
# Dockerデーモンを手動で起動
sudo dockerd &

# または、serviceコマンドを使用
sudo service docker start
```

### ユーザーがdockerグループに追加されていない

```bash
# 現在のユーザーを確認
whoami

# dockerグループに追加
sudo usermod -aG docker $USER

# WSLを再起動
exit
# Windows側で: wsl --shutdown
```

### 権限エラーが発生する

```bash
# dockerグループに所属しているか確認
groups

# dockerグループが表示されない場合、WSLを再起動
exit
# Windows側で: wsl --shutdown
```

---

## 🎯 デモンストレーション用起動

インストール完了後、デモンストレーション用に起動：

```bash
# 実行権限の付与
chmod +x demo-start.sh

# デモンストレーション用起動
./demo-start.sh
```

---

## 📝 よく使うコマンド

```bash
# Dockerサービスの起動
sudo service docker start
# または
sudo systemctl start docker

# Dockerサービスの停止
sudo service docker stop
# または
sudo systemctl stop docker

# Dockerサービスの状態確認
sudo systemctl status docker

# Dockerのバージョン確認
docker --version
docker compose version

# コンテナ一覧
docker ps

# イメージ一覧
docker images

# ログ確認
docker-compose logs -f
```

---

## ⚠️ 注意事項

1. **systemdの有効化**: WSL2でsystemdを使用する場合は、`/etc/wsl.conf`で有効化が必要です
2. **WSLの再起動**: ユーザーをdockerグループに追加した後は、WSLの再起動が必要です
3. **sudo権限**: Dockerサービスを起動する際は、初回のみsudo権限が必要な場合があります
4. **ネットワーク**: WSL内のDockerは、Windows側のファイアウォール設定に影響される場合があります

---

以上
