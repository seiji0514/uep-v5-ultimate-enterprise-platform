# WSL 内に Docker Engine を直接インストール

Docker Desktop for Windows を使わず、WSL 内で Docker を動かす手順。

---

## 前提

- Windows 10/11 で WSL 2 が有効
- Ubuntu などの Linux ディストリビューションがインストール済み

```powershell
# WSL バージョン確認
wsl -l -v
# VERSION が 2 であること
```

---

## 1. WSL を起動

```powershell
wsl
```

または、ターミナルで「Ubuntu」などを選択。

---

## 2. Docker 公式リポジトリを追加

```bash
# パッケージ更新
sudo apt update
sudo apt install -y ca-certificates curl gnupg

# Docker の GPG キー
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# リポジトリ登録（Ubuntu の場合）
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

**Debian の場合:**
```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

---

## 3. Docker をインストール

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

---

## 4. ユーザーを docker グループに追加

```bash
sudo usermod -aG docker $USER
```

**反映のため、いずれかを実行:**
```bash
newgrp docker
```
または WSL を一度終了して再起動。

---

## 5. Docker を起動

```bash
# 起動
sudo service docker start

# 自動起動（オプション）
echo 'sudo service docker start' >> ~/.bashrc
```

---

## 6. 動作確認

```bash
docker run hello-world
docker compose version
```

---

## 7. Unified Platform を起動

### 一括起動（推奨）

**Windows から（プロジェクトルートで）:**
```batch
scripts\wsl-unified-start.bat
```
※ パスが異なる場合は `WSL_ROOT` を編集

**WSL 内で:**
```bash
cd /mnt/c/uep-v5-ultimate-enterprise-platform/projects/unified-platform
bash scripts/wsl-start-all.sh
```

→ Docker 起動 → Unified Platform (app, db, redis) を一括起動

### 手動起動

```bash
cd /mnt/c/uep-v5-ultimate-enterprise-platform/projects/unified-platform
sudo service docker start
docker compose up -d
```

- API: http://localhost:8000
- Dashboard: http://localhost:8000/dashboard

---

## よくあるトラブル

| 現象 | 対処 |
|------|------|
| `Cannot connect to the Docker daemon` | `sudo service docker start` を実行 |
| `permission denied` | `newgrp docker` または WSL 再起動 |
| WSL 再起動で Docker が止まる | `~/.bashrc` に `sudo service docker start` を追加 |
| ポート 8000 が使えない | `docker compose down` で停止後、再起動 |
| init-db exit 1 | 解消済み。init-db を廃止し、app 起動時に seed を実行する方式に変更 |
| `invalid option` / `$'\r': command not found` | 改行コード CRLF が原因。`wsl-start-all.sh` を Cursor で開き、右下の「CRLF」をクリック→「LF」に変更して保存。または `scripts/fix-crlf.ps1` を実行 |
| `[sudo] password for xxx` | WSL のログインユーザー（kaho0525 など）のパスワードを入力 |
| `ERR_CONNECTION_REFUSED`（localhost:8000） | 1) `docker compose logs -f app` でエラー確認。2) app 初回起動は 10～20 秒かかる場合あり、少し待ってから再アクセス。3) コンテナ内疎通確認: `docker compose exec app python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/health').read())"`。4) `ports: "0.0.0.0:8000:8000"` に変更済み。5) それでも不通なら `docker compose down` 後、`wsl --shutdown`（PowerShellで）で WSL 再起動し、再度 `wsl-unified-start.bat` を実行 |

---

## 参考

- [Docker Engine インストール（Ubuntu）](https://docs.docker.com/engine/install/ubuntu/)
- [Docker Compose プラグイン](https://docs.docker.com/compose/install/linux/)
