# Git と バックアップ - 自分でやる手順

seiji0514 で管理。外部非公開の運用。

---

## 1. Git の基本手順

### 日常の流れ（作業の区切りごと）

```powershell
# 1. プロジェクトフォルダへ移動
cd C:\uep-v5-ultimate-enterprise-platform

# 2. 変更を確認
git status

# 3. 変更をステージング（全部）
git add .

# 4. コミット（メッセージを付ける）
git commit -m "feat: 〇〇を追加"

# 5. seiji0514 のリポジトリへプッシュ
git push origin main
```

### コミットメッセージの例

| 内容 | 例 |
|------|-----|
| 新機能 | `feat: 産業統合プラットフォームに〇〇を追加` |
| 修正 | `fix: ログインエラーを修正` |
| ドキュメント | `docs: バックアップ手順を更新` |

---

## 2. バックアップの手順

### 追加・更新のみ（N と O へ・日次推奨）

```cmd
cd C:\uep-v5-ultimate-enterprise-platform
scripts\一括バックアップ_更新のみ_N_GoogleDrive.bat
```

- **外付けドライブ N**: N:\uep-v5-backup
- **Google Drive O**: O:\uep-v5-backup

### 一括バックアップ（日付フォルダ作成・週次推奨）

```cmd
cd C:\uep-v5-ultimate-enterprise-platform
scripts\一括バックアップ_全先.bat
```

---

## 3. 新規システム構築時の目安

| タイミング | やること |
|------------|----------|
| 作業開始前 | `git status` でクリーンか確認 |
| 1機能できた | `git add .` → `git commit -m "feat: 〇〇"` |
| 1日終わり | コミット + 必要なら `git push` |
| 区切りごと | バックアップ（更新のみ） |

---

## 4. よく使うコマンド

```powershell
# 履歴確認
git log --oneline

# 直前のコミットを取り消し（変更は残す）
git reset --soft HEAD~1

# リモートの状態確認
git remote -v
```

---

## 5. トラブル時

| 状況 | 対処 |
|------|------|
| プッシュで認証エラー | GitHub の Personal Access Token でパスワード代わりに入力 |
| マージコンフリクト | `git status` で競合ファイルを確認し、手動で編集 |
| 間違えてコミット | `git reset --soft HEAD~1` で取り消し |
