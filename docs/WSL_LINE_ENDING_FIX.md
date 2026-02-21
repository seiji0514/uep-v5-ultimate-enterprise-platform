# WSL 改行コードエラー対処ガイド

**作成日**: 2026年1月29日  
**対象**: `$'\r': command not found` エラーが発生した場合

---

## 🚨 エラー: `install-docker-wsl.sh: line X: $'\r': command not found`

このエラーは、スクリプトファイルの改行コードがWindows形式（CRLF）になっている場合に発生します。LinuxではLF形式が必要です。

---

## ✅ 解決方法

### 方法1: sedコマンドで改行コードを変換（推奨）

WSLのUbuntuターミナルで：

```bash
# プロジェクトディレクトリに移動
cd /mnt/c/uep-v5-ultimate-enterprise-platform

# 改行コードをLFに変換
sed -i 's/\r$//' install-docker-wsl.sh

# 実行権限を付与
chmod +x install-docker-wsl.sh

# 実行
sudo bash install-docker-wsl.sh
```

### 方法2: dos2unixコマンドを使用（インストールが必要な場合）

```bash
# dos2unixをインストール（初回のみ）
sudo apt-get update
sudo apt-get install -y dos2unix

# プロジェクトディレクトリに移動
cd /mnt/c/uep-v5-ultimate-enterprise-platform

# 改行コードをLFに変換
dos2unix install-docker-wsl.sh

# 実行権限を付与
chmod +x install-docker-wsl.sh

# 実行
sudo bash install-docker-wsl.sh
```

### 方法3: スクリプトをWSL内で再作成

```bash
# プロジェクトディレクトリに移動
cd /mnt/c/uep-v5-ultimate-enterprise-platform

# 改行コードを変換してホームディレクトリにコピー
sed 's/\r$//' install-docker-wsl.sh > ~/install-docker-wsl.sh

# 実行権限を付与
chmod +x ~/install-docker-wsl.sh

# 実行
sudo bash ~/install-docker-wsl.sh
```

---

## 📋 完全な実行手順（推奨）

### ステップ1: プロジェクトディレクトリに移動

```bash
cd /mnt/c/uep-v5-ultimate-enterprise-platform
```

### ステップ2: 改行コードを変換

```bash
sed -i 's/\r$//' install-docker-wsl.sh
```

### ステップ3: 実行権限を付与

```bash
chmod +x install-docker-wsl.sh
```

### ステップ4: 実行

```bash
sudo bash install-docker-wsl.sh
```

---

## 🔍 改行コードの確認

```bash
# ファイルの改行コードを確認
file install-docker-wsl.sh

# または
hexdump -C install-docker-wsl.sh | head -5
```

CRLFの場合、`\r\n`（0x0D 0x0A）が表示されます。  
LFの場合、`\n`（0x0A）のみが表示されます。

---

## 🚨 トラブルシューティング

### sedコマンドが動作しない場合

```bash
# 別の方法で変換
tr -d '\r' < install-docker-wsl.sh > install-docker-wsl-fixed.sh
chmod +x install-docker-wsl-fixed.sh
sudo bash install-docker-wsl-fixed.sh
```

### sudoパスワードがわからない場合

rootユーザーで実行：

```bash
# Windows側のPowerShellまたはコマンドプロンプトで
wsl -u root

# WSL内で
cd /mnt/c/uep-v5-ultimate-enterprise-platform
sed -i 's/\r$//' install-docker-wsl.sh
chmod +x install-docker-wsl.sh
bash install-docker-wsl.sh
```

---

## ✅ 確認チェックリスト

- [ ] プロジェクトディレクトリに移動できた
- [ ] 改行コードを変換した（`sed -i 's/\r$//' install-docker-wsl.sh`）
- [ ] 実行権限を付与した（`chmod +x install-docker-wsl.sh`）
- [ ] `sudo bash install-docker-wsl.sh` を実行した
- [ ] sudoパスワードがわかる、またはrootユーザーで実行できる

---

## 🎯 ワンライナー（すべての手順を一度に実行）

```bash
cd /mnt/c/uep-v5-ultimate-enterprise-platform && sed -i 's/\r$//' install-docker-wsl.sh && chmod +x install-docker-wsl.sh && sudo bash install-docker-wsl.sh
```

---

以上
