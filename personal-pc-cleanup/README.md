# 個人用 PC 容量確保ツール

Docker クリーンアップと Cドライブの容量確保を行うスタンドアロンツール。  
**UEP v5.0・産業統合プラットフォーム・EOH とは無関係**です。

---

## 機能

| 機能 | 内容 |
|------|------|
| **Docker クリーンアップ** | 未使用コンテナ・イメージ・ボリューム・ビルドキャッシュの削除 |
| **Cドライブ スキャン** | node_modules, venv, __pycache__, ビルド成果物等の検出 |
| **一時フォルダ** | %TEMP%, ブラウザキャッシュ等の検出 |

---

## 必要環境

- **Python 3.8+**
- Cドライブスキャンはユーザーフォルダ等を走査するため、初回は数分かかることがあります
- **Docker**（Docker クリーンアップ利用時のみ。未インストールでも Cドライブスキャンは可能）

---

## 起動方法

### システム版（バックエンド + フロントエンド）※推奨

```cmd
start-standalone.bat
```

- バックエンド: http://localhost:5002
- フロントエンド: http://localhost:3002
- ブラウザで http://localhost:3002 を開く

### CLI 版（run.bat）

```cmd
run.bat
```

メニューから選択:
1. 検出のみ（削除しない）
2. Docker クリーンアップ実行
3. Cドライブ + 一時フォルダ スキャン＆削除
4. 全て実行

### コマンドライン

```cmd
REM 検出のみ
python cleanup.py --detect --all

REM Docker の使用量表示
python cleanup.py --detect --docker

REM Docker クリーンアップ実行
python cleanup.py --clean --docker

REM Cドライブの開発キャッシュ等をスキャン
python cleanup.py --detect --c-drive --temp

REM 削除実行（確認プロンプトあり）
python cleanup.py --clean --c-drive --temp
```

---

## Docker クリーンアップの内容

- `docker container prune` … 停止中コンテナ
- `docker image prune -a` … 未使用イメージ（タグ付き含む）
- `docker volume prune` … 未使用ボリューム
- `docker builder prune -a` … ビルドキャッシュ

**注意**: 未使用ボリューム削除でデータが消える場合があります。必要なボリュームは事前に確認してください。

---

## Docker VHDX の圧縮（Windows WSL2）

Docker Desktop が WSL2 を使っている場合、prune 後も `docker_data.vhdx` が縮まないことがあります。手動圧縮:

1. Docker Desktop を終了
2. `wsl --shutdown`
3. 管理者 PowerShell で:
   ```powershell
   Optimize-VHD -Path "$env:LOCALAPPDATA\Docker\wsl\disk\docker_data.vhdx" -Mode Full
   ```
4. Docker Desktop を再起動

---

## Cドライブ スキャン対象と判定

| 判定 | フォルダ名 | 説明 |
|------|------------|------|
| **削除可** | node_modules, venv, __pycache__, build, dist, .next, .nuxt, .cache 等 | 再生成可能 |
| **注意** | postgres_data, minio_data, prometheus_data, grafana_data | データが消える可能性あり |

- **削除可**: 緑バッジ表示。`npm install` / `pip install` 等で再生成可能
- **注意**: 赤バッジ表示。DB・ストレージの永続データ。重要なデータがある場合は削除しないこと

**除外**: `.git`, `Program Files`, Docker 本体はスキャンしません。

---

## 注意事項

- 削除前に必ず確認プロンプトが表示されます
- node_modules, venv 削除後は `npm install` / `pip install` で再生成が必要です
- 管理者権限は不要ですが、一部フォルダはアクセスできない場合があります
