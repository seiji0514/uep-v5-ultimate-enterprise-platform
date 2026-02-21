# WSL Windowsマウントポイントからのスクリプト実行エラー対処

**作成日**: 2026年1月29日  
**対象**: `/mnt/c/` から直接スクリプトを実行できない場合

---

## 🚨 エラー: `sudo: unable to execute /mnt/c/.../install-docker-wsl.sh: No such file or directory`

このエラーは、WSLでWindowsファイルシステム（`/mnt/c/`）上のスクリプトをsudoで直接実行する際に発生します。WindowsファイルシステムとLinuxファイルシステムの違いにより、実行権限やファイルシステムの制約が原因です。

---

## ✅ 解決方法

### 方法1: bash経由で実行（最も簡単・推奨）

```bash
# プロジェクトディレクトリに移動
cd /mnt/c/uep-v5-ultimate-enterprise-platform

# bash経由で実行
sudo bash install-docker-wsl.sh
```

### 方法2: スクリプトをWSLのホームディレクトリにコピーして実行

```bash
# プロジェクトディレクトリに移動
cd /mnt/c/uep-v5-ultimate-enterprise-platform

# ホームディレクトリにコピー
cp install-docker-wsl.sh ~/install-docker-wsl.sh

# 実行権限を付与
chmod +x ~/install-docker-wsl.sh

# 実行
sudo ~/install-docker-wsl.sh
```

### 方法3: スクリプトの内容を直接実行

```bash
# プロジェクトディレクトリに移動
cd /mnt/c/uep-v5-ultimate-enterprise-platform

# bash経由で実行（最も確実）
sudo bash install-docker-wsl.sh
```

### 方法4: rootユーザーで実行（sudoパスワードがわからない場合）

```bash
# Windows側のPowerShellまたはコマンドプロンプトで
wsl -u root

# WSL内で
cd /mnt/c/uep-v5-ultimate-enterprise-platform
bash install-docker-wsl.sh
```

---

## 📋 完全な実行手順（推奨）

### ステップ1: プロジェクトディレクトリに移動

```bash
cd /mnt/c/uep-v5-ultimate-enterprise-platform
```

### ステップ2: bash経由で実行

```bash
sudo bash install-docker-wsl.sh
```

これで実行できるはずです！

---

## 🔍 なぜこのエラーが発生するのか？

1. **ファイルシステムの違い**: Windowsファイルシステム（NTFS）とLinuxファイルシステム（ext4）の違い
2. **実行権限**: Windowsファイルシステム上のファイルは、Linuxの実行権限が正しく認識されない場合がある
3. **sudoの動作**: sudoは実行可能ファイルを直接実行しようとするが、Windowsマウントポイント上のファイルは特殊な扱いが必要

---

## 🚨 トラブルシューティング

### bash経由でも実行できない場合

```bash
# スクリプトの内容を確認
head -20 install-docker-wsl.sh

# スクリプトをWSLのホームディレクトリにコピー
cp install-docker-wsl.sh ~/
cd ~
chmod +x install-docker-wsl.sh
sudo ./install-docker-wsl.sh
```

### ファイルの改行コードの問題

Windowsで作成されたファイルは、改行コードがCRLFの場合があります：

```bash
# 改行コードを確認
file install-docker-wsl.sh

# 改行コードをLFに変換（必要に応じて）
dos2unix install-docker-wsl.sh
# または
sed -i 's/\r$//' install-docker-wsl.sh
```

---

## ✅ 確認チェックリスト

- [ ] プロジェクトディレクトリに移動できた
- [ ] `install-docker-wsl.sh` ファイルが存在する
- [ ] `sudo bash install-docker-wsl.sh` を試した
- [ ] sudoパスワードがわかる、またはrootユーザーで実行できる

---

## 🎯 推奨コマンド（ワンライナー）

```bash
cd /mnt/c/uep-v5-ultimate-enterprise-platform && sudo bash install-docker-wsl.sh
```

---

以上
