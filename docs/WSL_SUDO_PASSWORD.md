# WSL sudoパスワード設定ガイド

**作成日**: 2026年1月29日  
**対象**: WSL環境でsudoパスワードがわからない場合

---

## 🔐 sudoパスワードについて

WSL環境では、初回セットアップ時にユーザーアカウントを作成する際にパスワードを設定しています。パスワードを忘れた場合や設定していない場合は、以下の方法で対処できます。

---

## 📋 対処方法

### 方法1: sudoパスワードをリセット（推奨）

#### ステップ1: rootユーザーとしてWSLにログイン

Windows側のPowerShellまたはコマンドプロンプトで：

```powershell
# rootユーザーとしてWSLにログイン
wsl -u root
```

#### ステップ2: パスワードをリセット

WSL内で：

```bash
# 現在のユーザー名を確認（例: kaho0525）
whoami

# パスワードをリセット
passwd kaho0525
```

新しいパスワードを2回入力してください。

#### ステップ3: WSLを終了

```bash
exit
```

#### ステップ4: 通常ユーザーでWSLに再ログイン

通常通りWSL（Ubuntu）を起動し、設定したパスワードでsudoコマンドを実行できます。

---

### 方法2: パスワードなしでsudoを実行できるように設定（開発環境用）

**⚠️ 注意**: セキュリティ上の理由から、本番環境では推奨されません。開発環境でのみ使用してください。

#### ステップ1: rootユーザーとしてWSLにログイン

```powershell
# Windows側で
wsl -u root
```

#### ステップ2: sudoersファイルを編集

```bash
# visudoコマンドで編集（安全）
visudo

# または、直接編集
nano /etc/sudoers
```

#### ステップ3: 以下の行を追加

ファイルの最後に以下を追加：

```
kaho0525 ALL=(ALL) NOPASSWD: ALL
```

**注意**: `kaho0525` を実際のユーザー名に置き換えてください。

#### ステップ4: 保存して終了

- nanoの場合: `Ctrl + X` → `Y` → `Enter`
- visudoの場合: `Ctrl + X` → `Y` → `Enter`

#### ステップ5: WSLを終了

```bash
exit
```

これで、パスワードなしでsudoコマンドを実行できるようになります。

---

### 方法3: rootユーザーとして直接インストール（一時的な解決策）

**⚠️ 注意**: セキュリティ上の理由から、通常の作業では推奨されません。

#### ステップ1: rootユーザーとしてWSLにログイン

```powershell
# Windows側で
wsl -u root
```

#### ステップ2: プロジェクトディレクトリに移動

```bash
cd /mnt/c/uep-v5-ultimate-enterprise-platform
```

#### ステップ3: インストールスクリプトを実行（sudo不要）

```bash
chmod +x install-docker-wsl.sh
./install-docker-wsl.sh
```

**注意**: rootユーザーで実行する場合、スクリプト内のsudoは不要ですが、スクリプトはrootユーザーで実行されることを想定しています。

#### ステップ4: 通常ユーザーをdockerグループに追加

```bash
# 通常ユーザー名を確認（例: kaho0525）
# スクリプトが自動的に追加しますが、確認のため:
usermod -aG docker kaho0525
```

#### ステップ5: WSLを終了して再起動

```bash
exit
```

Windows側で：

```powershell
wsl --shutdown
```

その後、通常ユーザーでWSLを再起動してください。

---

## 🔍 現在のユーザー名を確認

```bash
# 現在のユーザー名を確認
whoami

# すべてのユーザーを確認
cat /etc/passwd | grep /home
```

---

## ✅ 推奨手順

1. **方法1（パスワードリセット）** を推奨します
   - セキュリティ上最も安全
   - 今後の作業でもパスワードが必要

2. **開発環境のみ** で方法2（パスワードなしsudo）を使用
   - 利便性が高い
   - セキュリティリスクあり

3. **一時的な解決策** として方法3（rootユーザー）を使用
   - インストールのみ実行
   - 通常作業は通常ユーザーで

---

## 🚨 トラブルシューティング

### rootユーザーでログインできない

```powershell
# WSLのデフォルトユーザーを確認
wsl --list --verbose

# デフォルトユーザーをrootに変更（一時的）
wsl --distribution Ubuntu --user root
```

### パスワードを設定したが、まだ認証できない

```bash
# sudoersファイルの構文エラーを確認
sudo visudo -c

# パスワードが正しく設定されているか確認
passwd -S kaho0525
```

---

## 📝 次のステップ

sudoパスワードの問題が解決したら、Dockerのインストールを続行してください：

```bash
cd /mnt/c/uep-v5-ultimate-enterprise-platform
chmod +x install-docker-wsl.sh
sudo ./install-docker-wsl.sh
```

---

以上
