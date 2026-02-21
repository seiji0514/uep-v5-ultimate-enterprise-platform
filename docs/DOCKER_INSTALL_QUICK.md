# Docker クイックインストールガイド（WSL）

**作成日**: 2026年1月29日  
**対象**: WSL環境でDockerを素早くインストールしたい場合

---

## 🚀 ワンライナーインストール

WSLのUbuntuターミナルで、以下のコマンドをコピー&ペーストして実行してください：

```bash
cd /mnt/c/uep-v5-ultimate-enterprise-platform && chmod +x install-docker-wsl.sh && sudo ./install-docker-wsl.sh
```

---

## 📋 詳細手順

### ステップ1: プロジェクトディレクトリに移動

```bash
cd /mnt/c/uep-v5-ultimate-enterprise-platform
```

### ステップ2: インストールスクリプトに実行権限を付与

```bash
chmod +x install-docker-wsl.sh
```

### ステップ3: Dockerをインストール（sudo権限が必要）

```bash
sudo ./install-docker-wsl.sh
```

インストールには数分かかります。途中でパスワードの入力が求められる場合があります。

---

## 🔄 WSLの再起動（必須）

インストール完了後、**必ずWSLを再起動**してください：

### WSL内で：

```bash
exit
```

### Windows側のPowerShellまたはコマンドプロンプトで：

```powershell
wsl --shutdown
```

### その後、再度WSL（Ubuntu）を起動

---

## ✅ インストール確認

WSLを再起動後、以下で確認：

```bash
# Dockerのバージョン確認
docker --version

# Docker Composeのバージョン確認
docker compose version

# Dockerサービスが起動しているか確認
sudo service docker status

# Dockerが動作しているか確認
docker ps
```

---

## 🚨 トラブルシューティング

### Dockerサービスが起動しない

```bash
# Dockerサービスを手動で起動
sudo service docker start

# または
sudo dockerd &
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

### systemdが使用できない

WSL2では、systemdがデフォルトで無効の場合があります。インストールスクリプトが自動的に `/etc/wsl.conf` を設定しますが、手動で確認する場合：

```bash
# /etc/wsl.confを確認
cat /etc/wsl.conf

# 以下の内容が含まれていることを確認:
# [boot]
# systemd=true
```

設定後、WSLを再起動してください。

---

## 🎯 次のステップ

Dockerのインストールが完了したら、デモンストレーションを起動できます：

```bash
# プロジェクトディレクトリに移動
cd /mnt/c/uep-v5-ultimate-enterprise-platform

# デモンストレーション起動
chmod +x demo-start.sh
./demo-start.sh
```

---

以上
