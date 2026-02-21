# トラブルシューティングガイド

**作成日**: 2026 年 1 月 29 日

---

## 🔧 よくある問題と解決方法

### 問題 1: バックエンドが起動しない（ImportError）

**エラーメッセージ**:

```
ImportError: cannot import name '_rate_limit_exceeded_handler' from 'slowapi.errors'
```

**解決方法**:

1. **slowapi を再インストール**:

```cmd
cd backend
venv\Scripts\activate
pip uninstall slowapi -y
pip install slowapi==0.1.9
```

2. **仮想環境を再作成**（推奨）:

```cmd
cd backend
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

### 問題 2: フロントエンドが起動しない

**エラーメッセージ**:

```
The system cannot find the path specified.
```

**解決方法**:

1. **フロントエンドディレクトリを確認**:

```cmd
dir frontend
```

2. **フロントエンドを手動で作成**:

```cmd
mkdir frontend
cd frontend
npx create-react-app . --template typescript
cd ..
```

3. **依存パッケージをインストール**:

```cmd
cd frontend
npm install
```

---

### 問題 3: ポートが既に使用されている

**エラーメッセージ**:

```
Address already in use
```

**解決方法**:

1. **ポートを使用しているプロセスを確認**:

```cmd
netstat -ano | findstr :8000
netstat -ano | findstr :3000
```

2. **プロセスを終了**:

```cmd
taskkill /F /PID <プロセスID>
```

3. **または、stop-all.bat を使用**:

```cmd
stop-all.bat
```

---

### 問題 4: Python が見つからない

**エラーメッセージ**:

```
'python' is not recognized as an internal or external command
```

**解決方法**:

1. **Python がインストールされているか確認**:

```cmd
python --version
```

2. **Python をインストール**: https://www.python.org/downloads/

3. **環境変数 PATH に追加**:
   - システムの環境変数に Python のパスを追加

---

### 問題 5: Node.js が見つからない

**エラーメッセージ**:

```
'node' is not recognized as an internal or external command
```

**解決方法**:

1. **Node.js がインストールされているか確認**:

```cmd
node --version
npm --version
```

2. **Node.js をインストール**: https://nodejs.org/

---

### 問題 6: 文字化け

**症状**: バッチファイルで日本語が文字化けする

**解決方法**:

1. **バッチファイルは既に修正済み**（`chcp 65001`が追加されています）

2. **コマンドプロンプトの文字コードを確認**:

```cmd
chcp
```

3. **UTF-8 に設定**（既にバッチファイル内で実行されています）:

```cmd
chcp 65001
```

---

### 問題 7: データベース接続エラー

**エラーメッセージ**:

```
could not connect to server
```

**解決方法**:

1. **PostgreSQL が起動しているか確認**

2. **SQLite を使用する場合**（開発環境）:

   - `.env`ファイルで`DATABASE_URL=sqlite:///./uep_db.sqlite`を設定

3. **PostgreSQL を使用する場合**:
   - PostgreSQL がインストールされ、起動していることを確認
   - `.env`ファイルで正しい接続文字列を設定

---

### 問題 8: Redis 接続エラー

**エラーメッセージ**:

```
Connection refused
```

**解決方法**:

1. **Redis が起動しているか確認**

2. **Redis なしで実行する場合**:
   - `.env`ファイルで`REDIS_URL`をコメントアウト
   - または、メモリベースのキャッシュを使用（自動的にフォールバック）

---

## 🚀 クイックフィックス

### 全てをリセットして再起動

```cmd
REM 1. 全サービスを停止
stop-all.bat

REM 2. 仮想環境を再作成
cd backend
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

REM 3. 再起動
cd ..
start-all.bat
```

---

### 問題 5: 起動時の警告メッセージ

**警告メッセージ**:

```
DeprecationWarning: on_event is deprecated, use lifespan event handlers instead.
UserWarning: Field name "schema" shadows an attribute in parent "BaseModel"
WARNING: You must pass the application as an import string to enable 'reload' or 'workers'.
```

**解決方法**:

これらの警告は既に修正済みです。以下の変更が適用されています：

1. **FastAPI の`on_event`を`lifespan`に変更**:

   - `@app.on_event("startup")`と`@app.on_event("shutdown")`を`@asynccontextmanager`を使用した`lifespan`関数に置き換えました
   - FastAPI の最新の推奨方法に準拠しています

2. **Pydantic の`schema`フィールド警告を修正**:

   - `backend/data_lake/models.py`の`CatalogCreate`と`CatalogUpdate`モデルに`model_config = {"protected_namespaces": ()}`を追加しました
   - これにより、`schema`フィールドが BaseModel の属性をシャドウしないようになります

3. **Uvicorn の reload 警告を修正**:
   - `reload=True`を使用する場合、アプリケーションをインポート文字列（`"main:app"`）として渡すように変更しました
   - これにより、reload 機能が正しく動作します

**確認方法**:
バックエンドを再起動して、警告が表示されないことを確認してください：

```cmd
cd backend
venv\Scripts\activate
python main.py
```

---

### 問題 6: `NameError: name 'performance_optimizer' is not defined`

**エラーメッセージ**:

```
NameError: name 'performance_optimizer' is not defined
File "C:\uep-v5-ultimate-enterprise-platform\backend\main.py", line 245, in add_request_id
```

**解決方法**:

`performance_optimizer`のインポートと使用を安全に処理するように修正しました：

1. **インポートを try-except で囲む**:

```python
# Phase 4: 最適化モジュールのインポート（オプショナル）
try:
    from optimization.performance import performance_optimizer
    from optimization.routes import router as optimization_router
    OPTIMIZATION_AVAILABLE = True
except ImportError as e:
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(f"Optimization module not available: {e}")
    OPTIMIZATION_AVAILABLE = False
    performance_optimizer = None
    optimization_router = None
```

2. **使用箇所で None チェックを追加**:

```python
# パフォーマンスメトリクスを記録（利用可能な場合）
if performance_optimizer:
    try:
        performance_optimizer.record_request(
            endpoint=request.url.path,
            response_time=duration,
            is_error=(response.status_code >= 400)
        )
    except Exception as e:
        # パフォーマンス記録のエラーはログに記録するが、リクエスト処理は続行
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to record performance metrics: {e}")
```

3. **ルーターの追加も条件付きに**:

```python
# Phase 4: 最適化ルーターを追加（利用可能な場合）
if OPTIMIZATION_AVAILABLE and optimization_router:
    app.include_router(optimization_router)
```

これにより、`performance_optimizer`が利用できない場合でも、アプリケーションは正常に動作します。

**確認方法**:
バックエンドを再起動して、エラーが解決されたことを確認してください：

```cmd
cd backend
venv\Scripts\activate
python main.py
```

その後、`http://localhost:8000` と `http://localhost:8000/docs` にアクセスして、正常に動作することを確認してください。

---

### 問題 7: 起動時の警告メッセージ（完全修正版）

**警告メッセージ**:

```
UserWarning: Field name "schema" shadows an attribute in parent "BaseModel"
Kafka not available: No module named 'kafka.vendor.six.moves'
UserWarning: pkg_resources is deprecated as an API
```

**解決方法**:

すべての警告を完全に修正しました：

1. **Pydantic の`schema`フィールド警告を抑制**:

   - `backend/main.py`の先頭に警告フィルターを追加

   ```python
   warnings.filterwarnings("ignore", message="Field name \"schema\" shadows an attribute in parent \"BaseModel\"")
   warnings.filterwarnings("ignore", category=UserWarning, module="pydantic._internal_fields")
   ```

2. **Kafka の警告を抑制**:

   - `backend/main.py`で Kafka ロガーのレベルを ERROR に設定
   - `backend/event_streaming/kafka_client.py`でも警告を抑制

   ```python
   logging.getLogger("kafka").setLevel(logging.ERROR)
   warnings.filterwarnings("ignore", message=".*kafka.*")
   ```

3. **pkg_resources の非推奨警告を抑制**:
   - `backend/main.py`で警告フィルターを追加
   - `backend/requirements.txt`に`setuptools<81.0.0`を追加して、非推奨 API を使用しないバージョンを固定
   ```python
   warnings.filterwarnings("ignore", message="pkg_resources is deprecated", category=UserWarning)
   ```

**確認方法**:
バックエンドを再起動して、警告が表示されないことを確認してください：

```cmd
cd backend
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**注意**: Windows のコマンドプロンプトでは`#`はコメントとして機能しません。コマンドラインにコメントを書かないでください。

これで、すべての警告が抑制され、クリーンな起動ログが表示されます。

---

## 📞 サポート

問題が解決しない場合は、以下を確認してください：

1. Python 3.11 以上がインストールされているか
2. Node.js 18 以上がインストールされているか
3. 必要なポート（8000, 3000）が使用可能か
4. ファイアウォールがブロックしていないか

---

以上
