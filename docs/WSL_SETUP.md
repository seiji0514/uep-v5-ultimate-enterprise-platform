# WSL環境でのセットアップガイド

**作成日**: 2026年1月29日  
**対象環境**: WSL2 (Ubuntu/Debian)

---

## 📋 前提条件

### 1. WSL2のインストール確認

```bash
# WSLバージョン確認
wsl --version

# WSL2が有効でない場合
wsl --set-default-version 2
```

### 2. Docker Desktop for Windowsのインストール

**推奨方法**: Docker Desktop for Windowsを使用（WSL2バックエンド）

1. [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)をダウンロード・インストール
2. Settings > General > "Use the WSL 2 based engine"を有効化
3. Settings > Resources > WSL Integrationで、使用するWSLディストリビューションを有効化

### 3. WSL内でDockerを直接インストール（推奨：Docker Desktopが使用できない場合）

**Docker Desktop for Windowsが使用できない環境（ノートPC等）の場合:**

詳細な手順は [WSL_DOCKER_INSTALL.md](WSL_DOCKER_INSTALL.md) を参照してください。

**クイックインストール:**

```bash
# 自動インストールスクリプトを使用
chmod +x install-docker-wsl.sh
sudo ./install-docker-wsl.sh

# WSLを再起動
exit
# Windows側で: wsl --shutdown
# 再度WSLを起動
```

---

## 🚀 セットアップ手順

### 1. プロジェクトディレクトリに移動

```bash
cd /mnt/d/AI_system_research/開発プロジェクト/AI\ system\ research\ and\ development\ track\ record/uep-v5-ultimate-enterprise-platform
```

または、WSL内にプロジェクトをコピー：

```bash
# Windows側のパスをWSL内にマウント
cd ~
mkdir -p uep-v5
cp -r /mnt/d/AI_system_research/開発プロジェクト/AI\ system\ research\ and\ development\ track\ record/uep-v5-ultimate-enterprise-platform/* ~/uep-v5/
cd ~/uep-v5
```

### 2. 実行権限の付与

```bash
chmod +x start.sh stop.sh restart.sh health-check.sh
```

### 3. サービスの起動

```bash
./start.sh
```

または手動で：

```bash
docker-compose up -d
```

---

## 🔍 動作確認

### ヘルスチェック

```bash
./health-check.sh
```

または個別に：

```bash
# Backend API
curl http://localhost:8000/health

# Kong経由
curl http://localhost:8002/api/v1/health

# Envoy経由
curl http://localhost:8080/api/v1/health
```

### ログ確認

```bash
# すべてのログ
docker-compose logs -f

# 特定のサービスのログ
docker-compose logs -f backend
docker-compose logs -f kong
```

### コンテナ状態確認

```bash
docker-compose ps
```

---

## 🛠️ トラブルシューティング

### Dockerが起動しない

```bash
# Dockerサービスの状態確認
sudo service docker status

# Dockerサービスの起動
sudo service docker start

# Docker Desktopを使用している場合、Windows側でDocker Desktopが起動しているか確認
```

### ポートが既に使用されている

```bash
# ポートの使用状況確認
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :8001

# 使用中のプロセスを終了
sudo kill -9 <PID>
```

### WSL2のメモリ不足

Windows側の `%UserProfile%\.wslconfig` を編集：

```ini
[wsl2]
memory=8GB
processors=4
swap=4GB
```

WSLを再起動：

```powershell
wsl --shutdown
```

---

## 📝 よく使うコマンド

```bash
# 起動
./start.sh

# 停止
./stop.sh

# 再起動
./restart.sh

# ヘルスチェック
./health-check.sh

# ログ確認
docker-compose logs -f

# コンテナ状態
docker-compose ps

# コンテナの再ビルド
docker-compose build --no-cache

# ボリュームも含めて完全削除
docker-compose down -v
```

---

## 🌐 サービスURL

- **Backend API**: http://localhost:8000
- **Kong Admin**: http://localhost:8001
- **Kong Proxy**: http://localhost:8002
- **Envoy Proxy**: http://localhost:8080
- **Envoy Admin**: http://localhost:9901
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin)

---

以上
