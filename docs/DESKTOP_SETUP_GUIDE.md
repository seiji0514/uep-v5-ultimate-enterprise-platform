# デスクトップPC移行・セットアップ指示書

**作成日**: 2026年1月29日  
**対象**: デスクトップPCでのデモンストレーション環境セットアップ

---

## 📋 前提条件

- デスクトップPCにWSL2がインストールされていること
- 管理者権限があること
- インターネット接続があること

---

## 🚀 セットアップ手順（ステップバイステップ）

### **ステップ1: WSL2の確認**

#### 1.1 WSL2がインストールされているか確認

**Windows側（PowerShellまたはコマンドプロンプト）**:

```powershell
# WSLバージョン確認
wsl --version

# WSLがインストールされていない場合
wsl --install

# WSL2をデフォルトに設定
wsl --set-default-version 2
```

#### 1.2 WSLディストリビューションの確認

```powershell
# インストール済みのディストリビューション確認
wsl --list --verbose

# Ubuntuがインストールされていない場合
wsl --install -d Ubuntu
```

---

### **ステップ2: プロジェクトファイルの移行**

#### 2.1 プロジェクトファイルをデスクトップPCにコピー

**方法1: USBメモリを使用**

1. ノートPCでプロジェクトフォルダをUSBメモリにコピー
2. デスクトップPCにUSBメモリを接続
3. プロジェクトフォルダをデスクトップPCにコピー

**推奨保存先**:
```
D:\AI_system_research\開発プロジェクト\AI system research and development track record\uep-v5-ultimate-enterprise-platform
```

**方法2: ネットワーク経由**

1. ノートPCとデスクトップPCを同じネットワークに接続
2. ファイル共有またはクラウドストレージを使用してコピー

**方法3: Gitを使用（推奨）**

```bash
# ノートPCでGitリポジトリにプッシュ
cd uep-v5-ultimate-enterprise-platform
git init
git add .
git commit -m "Initial commit"
git remote add origin <リポジトリURL>
git push -u origin main

# デスクトップPCでクローン
git clone <リポジトリURL>
cd uep-v5-ultimate-enterprise-platform
```

---

### **ステップ3: WSL内でDockerをインストール**

#### 3.1 WSLを起動

**Windows側**:

```powershell
# WSLを起動
wsl
```

または、スタートメニューから「Ubuntu」を起動

#### 3.2 プロジェクトディレクトリに移動

**WSL内**:

```bash
# Windows側のパスにアクセス
cd /mnt/d/AI_system_research/開発プロジェクト/AI\ system\ research\ and\ development\ track\ record/uep-v5-ultimate-enterprise-platform

# または、WSL内にコピー（推奨）
cd ~
mkdir -p projects
cp -r /mnt/d/AI_system_research/開発プロジェクト/AI\ system\ research\ and\ development\ track\ record/uep-v5-ultimate-enterprise-platform ~/projects/
cd ~/projects/uep-v5-ultimate-enterprise-platform
```

#### 3.3 Dockerのインストール

**WSL内**:

```bash
# 実行権限の付与
chmod +x install-docker-wsl.sh

# Dockerをインストール（sudo権限が必要）
sudo ./install-docker-wsl.sh
```

**手動インストールの場合**:

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

#### 3.4 WSLの再起動

**WSL内**:

```bash
exit
```

**Windows側（PowerShellまたはコマンドプロンプト）**:

```powershell
# WSLをシャットダウン
wsl --shutdown

# 再度WSLを起動
wsl
```

#### 3.5 Dockerの動作確認

**WSL内**:

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

### **ステップ4: プロジェクトのセットアップ**

#### 4.1 プロジェクトディレクトリに移動

**WSL内**:

```bash
cd ~/projects/uep-v5-ultimate-enterprise-platform
# または
cd /mnt/d/AI_system_research/開発プロジェクト/AI\ system\ research\ and\ development\ track\ record/uep-v5-ultimate-enterprise-platform
```

#### 4.2 実行権限の付与

```bash
chmod +x *.sh
chmod +x install-docker-wsl.sh demo-start.sh start.sh stop.sh restart.sh health-check.sh start-local.sh
```

#### 4.3 環境設定ファイルの確認

```bash
# バックエンドの環境変数ファイルを確認
cd backend
ls -la .env.example

# .envファイルがない場合、.env.exampleをコピー
cp .env.example .env
```

---

### **ステップ5: デモンストレーション環境の起動**

#### 5.1 デモンストレーション用起動

**WSL内**:

```bash
# プロジェクトディレクトリに移動
cd ~/projects/uep-v5-ultimate-enterprise-platform

# デモンストレーション用起動
./demo-start.sh
```

**初回起動時は時間がかかります（イメージのダウンロード・ビルド）**

#### 5.2 起動確認

**WSL内**:

```bash
# ヘルスチェック
./health-check.sh

# または個別に確認
curl http://localhost:8000/health
curl http://localhost:8002/api/v1/health
curl http://localhost:8080/api/v1/health
```

**Windows側（ブラウザ）**:

- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Kong Admin: http://localhost:8001
- Kong Proxy: http://localhost:8002
- Envoy Proxy: http://localhost:8080
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)
- MinIO Console: http://localhost:9001 (minioadmin/minioadmin)

---

## 🔍 トラブルシューティング

### Dockerサービスが起動しない

**WSL内**:

```bash
# サービスの状態確認
sudo systemctl status docker

# サービスを起動
sudo systemctl start docker

# サービスを有効化（自動起動）
sudo systemctl enable docker
```

**systemdが使用できない場合**:

```bash
# /etc/wsl.confを編集
sudo nano /etc/wsl.conf
```

以下を追加：

```ini
[boot]
systemd=true
```

**WSLを再起動**:

```powershell
# Windows側で
wsl --shutdown
```

### ポートが既に使用されている

**WSL内**:

```bash
# ポートの使用状況確認
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :8001

# 使用中のプロセスを終了
sudo kill -9 <PID>
```

### ユーザーがdockerグループに追加されていない

**WSL内**:

```bash
# 現在のユーザーを確認
whoami

# dockerグループに追加
sudo usermod -aG docker $USER

# WSLを再起動
exit
# Windows側で: wsl --shutdown
```

### コンテナが起動しない

**WSL内**:

```bash
# コンテナの状態確認
docker-compose ps

# ログ確認
docker-compose logs

# コンテナの再起動
docker-compose restart

# 完全に再構築
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

---

## 📝 デモンストレーション前のチェックリスト

### ✅ セットアップ確認

- [ ] WSL2がインストールされている
- [ ] Dockerがインストールされている
- [ ] Dockerサービスが起動している
- [ ] プロジェクトファイルがデスクトップPCにコピーされている
- [ ] 実行権限が付与されている（chmod +x *.sh）

### ✅ 起動確認

- [ ] デモンストレーション用起動スクリプトが実行できる
- [ ] すべてのコンテナが起動している（docker-compose ps）
- [ ] ヘルスチェックが成功する（./health-check.sh）
- [ ] ブラウザで各サービスにアクセスできる

### ✅ デモンストレーション準備

- [ ] ブラウザでAPI Docsを開ける（http://localhost:8000/docs）
- [ ] Grafanaにログインできる（http://localhost:3000）
- [ ] Prometheusにアクセスできる（http://localhost:9090）
- [ ] デモンストレーション用のデータが準備されている（必要に応じて）

---

## 🎯 デモンストレーション時の操作手順

### 1. デモンストレーション開始前

```bash
# WSLを起動
wsl

# プロジェクトディレクトリに移動
cd ~/projects/uep-v5-ultimate-enterprise-platform

# デモンストレーション用起動
./demo-start.sh

# 起動確認（30秒待機後）
./health-check.sh
```

### 2. デモンストレーション中

**ブラウザで以下を開く**:

1. **API Docs**: http://localhost:8000/docs
   - APIの仕様を確認
   - エンドポイントをテスト

2. **Grafana**: http://localhost:3000
   - ダッシュボードを表示
   - メトリクスを確認

3. **Prometheus**: http://localhost:9090
   - メトリクスを確認
   - クエリを実行

### 3. デモンストレーション終了後

```bash
# サービスを停止
./stop.sh

# または
docker-compose down
```

---

## 📊 よく使うコマンド

### サービス管理

```bash
# 起動
./demo-start.sh

# 停止
./stop.sh

# 再起動
./restart.sh

# ヘルスチェック
./health-check.sh
```

### Docker操作

```bash
# コンテナ状態確認
docker-compose ps

# ログ確認
docker-compose logs -f

# 特定のサービスのログ
docker-compose logs -f backend
docker-compose logs -f kong

# コンテナの再起動
docker-compose restart backend

# 完全に再構築
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### デバッグ

```bash
# コンテナ内に入る
docker-compose exec backend bash

# 環境変数の確認
docker-compose exec backend env

# ネットワークの確認
docker network ls
docker network inspect uep-v5-ultimate-enterprise-platform_uep-network
```

---

## ⚠️ 注意事項

1. **WSLの再起動**: Dockerをインストールした後、ユーザーをdockerグループに追加した後は、WSLの再起動が必要です
2. **ポートの競合**: 他のアプリケーションが同じポートを使用している場合、エラーが発生します
3. **メモリ不足**: WSL2のメモリ制限を調整する場合は、Windows側の `.wslconfig` を編集してください
4. **ファイアウォール**: Windows側のファイアウォールがポートをブロックしている場合があります

---

## 📞 サポート

問題が発生した場合：

1. **ログを確認**: `docker-compose logs`
2. **ヘルスチェックを実行**: `./health-check.sh`
3. **ドキュメントを確認**: `docs/` フォルダ内のドキュメントを参照

---

## ✅ 完了確認

以下のすべてが動作していれば、セットアップ完了です：

- ✅ Dockerがインストールされている
- ✅ すべてのコンテナが起動している
- ✅ ヘルスチェックが成功する
- ✅ ブラウザで各サービスにアクセスできる

---

以上
