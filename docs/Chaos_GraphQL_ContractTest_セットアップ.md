# Chaos Engineering / GraphQL / Contract Test セットアップ

## 404 が表示される場合の対処

### 診断手順

1. **診断エンドポイントの確認**
   - http://localhost:8000/chaos-ok にアクセス
   - `{"status": "ok", "message": "Chaos/GraphQL routes are in this build"}` が返れば、main.py の変更が反映されている
   - 404 の場合は、**別のプロセス**が port 8000 を使用している可能性あり

2. **port 8000 の使用状況確認（PowerShell）**
   ```powershell
   netstat -ano | findstr :8000
   ```
   - 表示された PID が想定外のプロセスの場合、そのプロセスを終了

3. **キャッシュ削除と再起動**
   ```bat
   cd backend
   rmdir /s /q __pycache__ 2>nul
   for /d /r . %d in (__pycache__) do @if exist "%d" rmdir /s /q "%d" 2>nul
   ```
   その後、`start-backend.bat` を再実行

4. **Docker 使用時**
   - docker-compose で起動している場合、port 8000 はコンテナのバックエンドが使用
   - ローカルの `start-backend.bat` と競合するため、どちらか一方のみ起動すること

---

### 1. 依存パッケージのインストール

**GraphQL** には `strawberry-graphql` が必要です。

```bash
cd backend
pip install strawberry-graphql[fastapi]
```

または一括インストール：

```bash
cd backend
pip install -r requirements.txt
```

### 2. バックエンドの再起動

コード変更後は必ずバックエンドを再起動してください。

- **start-backend.bat 使用時**: Ctrl+C で停止 → 再度 `start-backend.bat` を実行
- **手動起動時**: `python main.py` を再実行

### 3. 起動ログの確認

起動時に次のメッセージが出ていないか確認してください。

- `Chaos module not available` → chaos モジュールのインポート失敗
- `GraphQL module not available` → strawberry 未インストール、または `graphql` モジュール名衝突（`graphql_api` にリネーム済み）

### 4. 動作確認

| 機能 | URL | 期待される結果 |
|------|-----|----------------|
| Chaos status | http://localhost:8000/api/v1/chaos/status | JSON（enabled, endpoints 等） |
| GraphQL | http://localhost:8000/graphql | GraphiQL IDE 画面 |
| ルート | http://localhost:8000/ | `"graphql": "/graphql"` が含まれる |

---

## Contract Test の実行方法

### 前提

- バックエンドの `backend` ディレクトリで実行する
- `pytest` がインストール済み（`requirements.txt` に含まれる）

### 実行コマンド

```bash
cd backend
pytest tests/contract/ -v
```

**推奨**（カバレッジエラーを避ける場合）:
```bash
cd backend
pytest tests/contract/ -v --no-cov
```

**仮想環境を使用する場合**:
```bash
cd backend
call venv\Scripts\activate.bat   # Windows
# source venv/bin/activate      # Linux/Mac
pytest tests/contract/ -v --no-cov
```

### 実行例

```
tests/contract/test_contract_auth.py::TestAuthLoginContract::test_login_returns_required_fields PASSED
tests/contract/test_contract_auth.py::TestAuthLoginContract::test_login_rejects_invalid_credentials PASSED
tests/contract/test_contract_auth.py::TestAuthMeContract::test_me_returns_user_info_with_valid_token PASSED
...
```

### バックエンドを起動せずにテストする場合

Contract Test は FastAPI の `TestClient` を使用しているため、**バックエンドを起動していなくても**テストできます。`TestClient` がアプリを内部で起動します。

### トラブルシューティング

| 現象 | 対処 |
|------|------|
| `ModuleNotFoundError: No module named 'main'` | `cd backend` で backend ディレクトリに移動してから実行 |
| `ModuleNotFoundError: No module named 'chaos'` | 同上 |
| 認証テストが失敗 | デモユーザー（developer/dev123）が有効か確認 |
