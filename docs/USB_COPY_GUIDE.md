# USBドライブへのコピー手順

CドライブからUSBドライブ（N: 等）へコピーする際のエラー対策ガイド。

---

## エラーの主な原因

| 原因 | 説明 |
|------|------|
| **パス長制限** | Windows の 260 文字制限。`node_modules` 内の深いパスで発生しやすい |
| **ファイル数** | `node_modules` は数万ファイルあり、コピーに時間がかかりエラーになりやすい |
| **venv** | Python 仮想環境のシンボリックリンクが USB（exFAT 等）で失敗することがある |

---

## 推奨方法: 除外コピースクリプト

### 手順

1. **`scripts\copy-to-usb.bat` を実行**
   - `node_modules`、`venv`、`__pycache__` を除外してコピー
   - パス長・ファイル数によるエラーを回避

2. **コピー先のドライブを変更する場合**
   - `copy-to-usb.bat` を開く
   - `set DEST=N:\uep-v5-ultimate-enterprise-platform` の `N:` を変更（例: `E:`）

3. **コピー完了後、USB 上で起動**
   - USB のフォルダで `start-local.bat` を実行
   - `venv` と `node_modules` が自動作成される（初回は数分かかります）

---

## 手動でコピーする場合

1. 次のフォルダ・ファイルを**コピーしない**（除外）:
   - `backend\venv`
   - `frontend\node_modules`
   - `backend\__pycache__`
   - `**\__pycache__`
   - `.git`（Git 管理が不要な場合）

2. それ以外を USB にコピー

3. USB 上で `start-local.bat` を実行

---

## 7-Zip でアーカイブしてコピーする方法

1. 除外フォルダを除いて 7-Zip で圧縮
2. 生成した zip を USB にコピー
3. USB 上で解凍
4. `start-local.bat` を実行

---

## トラブルシューティング

| 現象 | 対処 |
|------|------|
| N: ドライブが見つからない | USB を接続し、エクスプローラーでドライブレターを確認 |
| 削除できません | コピー先フォルダを手動で削除してから再実行 |
| コピーが遅い | USB 3.0 以上を使用。除外コピーで `node_modules` を省く |
