# Dockerインストールエラー対処ガイド

**作成日**: 2026年1月29日  
**対象**: `No such file or directory` エラーが発生した場合

---

## 🚨 エラー: `sudo: unable to execute ./install-docker-wsl.sh: No such file or directory`

このエラーは、sudoで実行する際に現在のディレクトリが正しく設定されていない場合に発生します。

---

## ✅ 解決方法

### 方法1: 絶対パスで実行（推奨）

```bash
# プロジェクトディレクトリに移動
cd /mnt/c/uep-v5-ultimate-enterprise-platform

# ファイルの存在確認
ls -la install-docker-wsl.sh

# 絶対パスで実行
sudo /mnt/c/uep-v5-ultimate-enterprise-platform/install-docker-wsl.sh
```

### 方法2: 実行権限を付与してから絶対パスで実行

```bash
# プロジェクトディレクトリに移動
cd /mnt/c/uep-v5-ultimate-enterprise-platform

# 実行権限を付与
chmod +x install-docker-wsl.sh

# 絶対パスで実行
sudo /mnt/c/uep-v5-ultimate-enterprise-platform/install-docker-wsl.sh
```

### 方法3: sudo -E オプションを使用（環境変数を保持）

```bash
# プロジェクトディレクトリに移動
cd /mnt/c/uep-v5-ultimate-enterprise-platform

# 実行権限を付与
chmod +x install-docker-wsl.sh

# sudo -E で実行（環境変数を保持）
sudo -E ./install-docker-wsl.sh
```

### 方法4: rootユーザーで直接実行（sudoパスワードがわからない場合）

```bash
# Windows側のPowerShellまたはコマンドプロンプトで
wsl -u root

# WSL内で
cd /mnt/c/uep-v5-ultimate-enterprise-platform
chmod +x install-docker-wsl.sh
./install-docker-wsl.sh
```

**注意**: rootユーザーで実行する場合、sudoは不要です。

---

## 🔍 ファイルの存在確認

まず、ファイルが存在するか確認してください：

```bash
# プロジェクトディレクトリに移動
cd /mnt/c/uep-v5-ultimate-enterprise-platform

# ファイルの存在確認
ls -la install-docker-wsl.sh

# ファイルの内容を確認（最初の数行）
head -5 install-docker-wsl.sh
```

---

## 📋 完全な実行手順（推奨）

### ステップ1: プロジェクトディレクトリに移動

```bash
cd /mnt/c/uep-v5-ultimate-enterprise-platform
```

### ステップ2: ファイルの存在確認

```bash
ls -la install-docker-wsl.sh
```

### ステップ3: 実行権限を付与

```bash
chmod +x install-docker-wsl.sh
```

### ステップ4: 絶対パスで実行

```bash
sudo /mnt/c/uep-v5-ultimate-enterprise-platform/install-docker-wsl.sh
```

または、sudoパスワードがわからない場合：

```bash
# Windows側で rootユーザーとしてWSLにログイン
# PowerShell: wsl -u root

# WSL内で
cd /mnt/c/uep-v5-ultimate-enterprise-platform
chmod +x install-docker-wsl.sh
./install-docker-wsl.sh
```

---

## 🚨 トラブルシューティング

### ファイルが見つからない場合

```bash
# 現在のディレクトリを確認
pwd

# ファイルを検索
find /mnt/c -name "install-docker-wsl.sh" 2>/dev/null

# プロジェクトディレクトリの内容を確認
ls -la /mnt/c/uep-v5-ultimate-enterprise-platform/
```

### パスの問題

WSLでは、Windowsのパスは `/mnt/c/` としてマウントされます。

- Windows: `C:\uep-v5-ultimate-enterprise-platform`
- WSL: `/mnt/c/uep-v5-ultimate-enterprise-platform`

### 権限の問題

```bash
# ファイルの権限を確認
ls -la install-docker-wsl.sh

# 実行権限を付与
chmod +x install-docker-wsl.sh

# 所有者を確認
ls -l install-docker-wsl.sh
```

---

## ✅ 確認チェックリスト

- [ ] プロジェクトディレクトリに移動できた
- [ ] `install-docker-wsl.sh` ファイルが存在する
- [ ] ファイルに実行権限がある（`chmod +x`）
- [ ] sudoパスワードがわかる、またはrootユーザーで実行できる
- [ ] 絶対パスで実行している

---

以上
