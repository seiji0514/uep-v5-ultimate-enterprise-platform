# WSL環境での手動デモンストレーション実行ガイド

**作成日**: 2026年1月29日  
**対象**: CursorからWSLコマンドが実行できない場合の手動実行手順

---

## 🚨 エラー対処方法

`Wsl/Service/CreateInstance/E_ACCESSDENIED` エラーが発生した場合、以下の手順でWSL内で直接実行してください。

---

## 📋 手動実行手順

### ステップ1: WSLを起動

Windows側で以下のいずれかの方法でWSLを起動：

1. **PowerShellまたはコマンドプロンプトから:**

   ```powershell
   wsl
   ```

2. **Windows Terminalから:**
   - Windows Terminalを開く
   - タブで「Ubuntu」または使用しているWSLディストリビューションを選択

3. **スタートメニューから:**
   - 「Ubuntu」を検索して起動

---

### ステップ2: プロジェクトディレクトリに移動

WSL内で以下のコマンドを実行：

```bash
# WindowsのCドライブは /mnt/c/ としてマウントされます
cd /mnt/c/uep-v5-ultimate-enterprise-platform

# または、プロジェクトが別の場所にある場合
# cd /mnt/d/path/to/uep-v5-ultimate-enterprise-platform

# 現在のディレクトリを確認
pwd
ls -la
```

---

### ステップ3: Dockerの状態を確認

```bash
# Dockerのバージョン確認
docker --version

# Docker Composeのバージョン確認
docker compose version

# Dockerサービスの状態確認
sudo service docker status

# Dockerサービスが起動していない場合、起動
sudo service docker start

# Dockerが動作しているか確認
docker ps
```

---

### ステップ4: Dockerがインストールされていない場合

Dockerがインストールされていない場合は、以下のコマンドでインストール：

```bash
# 実行権限を付与
chmod +x install-docker-wsl.sh

# Dockerをインストール（sudo権限が必要）
sudo ./install-docker-wsl.sh

# WSLを再起動（Windows側で実行）
# exit でWSLを終了
# Windows側で: wsl --shutdown
# 再度WSLを起動
```

---

### ステップ5: デモンストレーションを起動

```bash
# 実行権限を付与（初回のみ）
chmod +x demo-start.sh

# デモンストレーション用起動スクリプトを実行
./demo-start.sh
```

**または、手動で実行:**

```bash
# 1. 既存のコンテナを停止・削除
docker compose down -v

# 2. イメージのビルド（初回は時間がかかります）
docker compose build

# 3. コンテナの起動
docker compose up -d

# 4. サービスの起動確認（30秒待機）
sleep 30

# 5. コンテナの状態確認
docker compose ps
```

---

### ステップ6: ヘルスチェック

```bash
# ヘルスチェックスクリプトを実行
chmod +x health-check.sh
./health-check.sh

# または、個別に確認
curl http://localhost:8000/health
curl http://localhost:8002/api/v1/health
curl http://localhost:8080/api/v1/health
```

---

## 📊 サービスURL

起動後、以下のURLでアクセス可能：

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Kong Admin**: http://localhost:8001
- **Kong Proxy**: http://localhost:8002
- **Envoy Proxy**: http://localhost:8080
- **Envoy Admin**: http://localhost:9901
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000
  - ユーザー名: `admin`
  - パスワード: `admin`
- **MinIO Console**: http://localhost:9001
  - ユーザー名: `minioadmin`
  - パスワード: `minioadmin`

---

## 🔍 トラブルシューティング

### Dockerサービスが起動しない

```bash
# systemdが使用できない場合
sudo service docker start

# または、手動でDockerデーモンを起動
sudo dockerd &
```

### ポートが既に使用されている

```bash
# ポートの使用状況確認
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :8001

# 使用中のプロセスを終了
sudo kill -9 <PID>
```

### コンテナが起動しない

```bash
# ログを確認
docker compose logs

# 特定のサービスのログを確認
docker compose logs backend
docker compose logs kong

# コンテナの状態を確認
docker compose ps
```

### 権限エラーが発生する

```bash
# 現在のユーザーを確認
whoami

# dockerグループに追加（必要に応じて）
sudo usermod -aG docker $USER

# WSLを再起動
exit
# Windows側で: wsl --shutdown
```

---

## 🛑 停止方法

```bash
# 停止スクリプトを使用
chmod +x stop.sh
./stop.sh

# または、手動で停止
docker compose down

# ボリュームも含めて完全削除
docker compose down -v
```

---

## 📝 よく使うコマンド

```bash
# コンテナの状態確認
docker compose ps

# ログ確認（リアルタイム）
docker compose logs -f

# 特定のサービスのログ
docker compose logs -f backend

# コンテナの再起動
docker compose restart backend

# イメージの再ビルド
docker compose build --no-cache backend

# すべてのコンテナとボリュームを削除
docker compose down -v
```

---

## ✅ 確認チェックリスト

- [ ] WSLが起動している
- [ ] プロジェクトディレクトリに移動できた
- [ ] Dockerがインストールされている
- [ ] Dockerサービスが起動している
- [ ] `demo-start.sh` が実行できる
- [ ] コンテナが起動している
- [ ] ヘルスチェックが成功している
- [ ] ブラウザでサービスにアクセスできる

---

以上
