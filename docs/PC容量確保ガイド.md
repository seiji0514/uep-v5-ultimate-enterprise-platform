# PC容量確保ガイド

UEP v5.0 プロジェクト内で、圧縮・削除・検出が可能な箇所の一覧と手順です。

---

## 1. 削除・圧縮可能な箇所（一覧）

| 箇所 | 説明 | 削除後の復元 |
|------|------|--------------|
| **node_modules/** | フロントエンドの npm パッケージ | `npm install` で再生成 |
| **venv/** | Python 仮想環境 | `pip install -r requirements.txt` で再生成 |
| **__pycache__/** | Python バイトコードキャッシュ | 実行時に自動生成 |
| **.pytest_cache/** | Pytest キャッシュ | テスト実行時に自動生成 |
| **build/**, **dist/** | ビルド成果物 | `npm run build` で再生成 |
| **htmlcov/**, **.coverage**, **coverage.xml** | カバレッジレポート | `pytest --cov` で再生成 |
| ***.db**, ***.sqlite** | SQLite データベース | 起動時に再作成（サンプルデータは再投入） |
| **minio_data/** | MinIO オブジェクトストレージ | Docker 起動時に再作成 |
| **postgres_data/** | PostgreSQL データ | Docker 起動時に再作成 |
| **prometheus_data/** | Prometheus メトリクス | Docker 起動時に再作成 |
| **grafana_data/** | Grafana ダッシュボード | Docker 起動時に再作成 |

---

## 2. 検出・一括削除スクリプト

### 検出のみ（削除しない）

```powershell
powershell -ExecutionPolicy Bypass -File scripts\disk-space-cleanup.ps1 -DetectOnly
```

### 削除を実行

```powershell
powershell -ExecutionPolicy Bypass -File scripts\disk-space-cleanup.ps1 -Clean
```

確認プロンプトで `y` を入力すると削除が実行されます。

---

## 3. 手動削除の例

### Python キャッシュのみ削除（安全）

```powershell
Get-ChildItem -Path . -Include __pycache__, .pytest_cache -Recurse -Directory | Remove-Item -Recurse -Force
```

### node_modules の容量確認

```powershell
Get-ChildItem -Path . -Filter node_modules -Recurse -Directory | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "$($_.FullName): $([math]::Round($size, 1)) MB"
}
```

### venv 削除（backend のみ）

```batch
rmdir /s /q backend\venv
```

削除後は `start-backend.bat` または `rebuild-backend-simple.bat` で再作成。

---

## 4. WSL 利用時の VHDX 圧縮

WSL の仮想ディスク（ext4.vhdx）が肥大化している場合:

1. WSL をシャットダウン: `wsl --shutdown`
2. `diskpart_compact.txt` の内容に従い diskpart で compact を実行

```diskpart
select vdisk file="C:\Users\<ユーザー名>\AppData\Local\wsl\<ID>\ext4.vhdx"
compact vdisk
exit
```

※ パスは `%LOCALAPPDATA%\wsl` 内の ext4.vhdx を確認してください。

---

## 5. 注意事項

| 項目 | 説明 |
|------|------|
| **node_modules / venv** | 削除後は再インストールに数分かかります |
| **.git** | 削除しないでください（リポジトリが壊れます） |
| **DB ファイル** | 手動で投入したデータは消えます。サンプルデータは再投入されます |
| **Docker データ** | minio_data 等を削除すると、保存済みオブジェクトは消えます |

---

## 6. サブプロジェクトについて

次のサブプロジェクトにも `node_modules` や `venv` が存在する場合があります:

- `frontend/`
- `enterprise_operations_hub/frontend/`
- `industry_unified_platform/frontend/`
- `medical/`, `space/`, `traffic/` 内の各プロジェクト

スクリプトはプロジェクト全体を再帰検索するため、これらも検出・削除対象になります。
