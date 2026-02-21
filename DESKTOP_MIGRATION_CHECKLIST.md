# デスクトップPC移行チェックリスト

**作成日**: 2026年1月29日  
**用途**: ノートPCからデスクトップPCへの移行時の確認項目

---

## 📋 移行前の準備（ノートPC）

### ✅ ファイルの確認

- [ ] プロジェクトフォルダが存在する
- [ ] すべてのファイルがコピー可能な状態である
- [ ] Gitリポジトリにコミット・プッシュ済み（推奨）

### ✅ 必要な情報の記録

- [ ] プロジェクトのパス
- [ ] 使用しているポート番号
- [ ] 環境変数の設定内容（.envファイル）
- [ ] カスタム設定の内容

---

## 🚀 デスクトップPCでのセットアップ

### ✅ ステップ1: WSL2の確認

- [ ] WSL2がインストールされている
- [ ] Ubuntu（または他のディストリビューション）がインストールされている
- [ ] WSL2がデフォルトに設定されている

**確認コマンド**:
```powershell
wsl --version
wsl --list --verbose
```

### ✅ ステップ2: プロジェクトファイルの移行

- [ ] プロジェクトフォルダをデスクトップPCにコピー
- [ ] ファイルが正しくコピーされている（ファイル数・サイズを確認）
- [ ] プロジェクトディレクトリに移動できる

**確認コマンド**:
```bash
cd ~/projects/uep-v5-ultimate-enterprise-platform
ls -la
```

### ✅ ステップ3: Dockerのインストール

- [ ] Dockerがインストールされている
- [ ] Dockerサービスが起動している
- [ ] 現在のユーザーがdockerグループに所属している
- [ ] Dockerがsudoなしで実行できる

**確認コマンド**:
```bash
docker --version
docker compose version
docker ps
```

### ✅ ステップ4: プロジェクトのセットアップ

- [ ] 実行権限が付与されている
- [ ] 環境変数ファイル（.env）が存在する
- [ ] 必要な設定ファイルが存在する

**確認コマンド**:
```bash
chmod +x *.sh
ls -la *.sh
ls -la backend/.env
```

### ✅ ステップ5: デモンストレーション環境の起動

- [ ] デモンストレーション用起動スクリプトが実行できる
- [ ] すべてのコンテナが起動している
- [ ] ヘルスチェックが成功する
- [ ] ブラウザで各サービスにアクセスできる

**確認コマンド**:
```bash
./demo-start.sh
./health-check.sh
docker-compose ps
```

---

## 🔍 動作確認項目

### ✅ バックエンドAPI

- [ ] http://localhost:8000 にアクセスできる
- [ ] http://localhost:8000/health が正常に応答する
- [ ] http://localhost:8000/docs が表示される

### ✅ API Gateway

- [ ] http://localhost:8002/api/v1/health が正常に応答する（Kong経由）
- [ ] http://localhost:8080/api/v1/health が正常に応答する（Envoy経由）
- [ ] http://localhost:8001 にアクセスできる（Kong Admin）

### ✅ 監視基盤

- [ ] http://localhost:9090 にアクセスできる（Prometheus）
- [ ] http://localhost:3000 にアクセスできる（Grafana）
- [ ] Grafanaにログインできる（admin/admin）

### ✅ データレイク

- [ ] http://localhost:9001 にアクセスできる（MinIO Console）
- [ ] MinIO Consoleにログインできる（minioadmin/minioadmin）

---

## 🛠️ トラブルシューティング

### ❌ Dockerがインストールされていない

**対応**:
```bash
sudo ./install-docker-wsl.sh
```

### ❌ Dockerサービスが起動しない

**対応**:
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### ❌ ポートが既に使用されている

**対応**:
```bash
sudo netstat -tulpn | grep :8000
sudo kill -9 <PID>
```

### ❌ コンテナが起動しない

**対応**:
```bash
docker-compose logs
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

---

## 📝 デモンストレーション前の最終確認

### ✅ 起動確認

- [ ] すべてのコンテナが起動している
- [ ] ヘルスチェックが成功する
- [ ] ログにエラーがない

### ✅ アクセス確認

- [ ] ブラウザで各サービスにアクセスできる
- [ ] API Docsが表示される
- [ ] Grafanaにログインできる

### ✅ デモンストレーション準備

- [ ] デモンストレーション用のデータが準備されている（必要に応じて）
- [ ] スクリーンショットが準備されている（必要に応じて）
- [ ] 説明資料が準備されている（必要に応じて）

---

## 🎯 デモンストレーション時の手順

### 1. 起動

```bash
./demo-start.sh
```

### 2. 確認

```bash
./health-check.sh
```

### 3. ブラウザで確認

- API Docs: http://localhost:8000/docs
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090

### 4. 停止

```bash
./stop.sh
```

---

## ✅ 完了

すべてのチェック項目が完了していれば、デスクトップPCでのセットアップは完了です。

デモンストレーションを開始できます。

---

以上
