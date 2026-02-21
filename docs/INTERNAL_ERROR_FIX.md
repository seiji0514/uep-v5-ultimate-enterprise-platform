# 内部エラー修正ガイド

**作成日**: 2026年1月29日

---

## 🔧 問題

バックエンドは起動していますが、以下のURLで内部エラーが発生：

- `http://localhost:8000/` → INTERNAL_ERROR
- `http://localhost:8000/docs` → INTERNAL_ERROR

---

## ✅ 修正内容

### 1. ルートエンドポイントの追加

`backend/main.py`にルートエンドポイント`/`を追加：

```python
@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "UEP v5.0 - Ultimate Enterprise Platform",
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "health": "/health",
        "api": "/api/v1"
    }
```

### 2. 公開エンドポイントの設定

ゼロトラストポリシーの評価から公開エンドポイントを除外：

- `/` - ルート
- `/health` - ヘルスチェック
- `/metrics` - メトリクス
- `/docs` - APIドキュメント
- `/redoc` - ReDoc
- `/openapi.json` - OpenAPI仕様

### 3. デバッグモードの有効化

`.env`ファイルに以下を追加：

```
DEBUG=true
ENVIRONMENT=development
```

これにより、エラーの詳細情報が表示されます。

### 4. エラーハンドラーの改善

デバッグモード時に詳細なエラー情報（トレースバック）を表示するように改善。

---

## 🚀 再起動

修正後、バックエンドを再起動：

```cmd
cd backend
python main.py
```

または：

```cmd
start-backend.bat
```

---

## 📝 確認

以下のURLにアクセスして動作確認：

- **ルート**: http://localhost:8000/
- **API Docs**: http://localhost:8000/docs
- **ヘルスチェック**: http://localhost:8000/health
- **API**: http://localhost:8000/api/v1/health

---

## 🔍 エラーの詳細確認

デバッグモードが有効になっている場合、エラーレスポンスに詳細な情報が含まれます：

```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "具体的なエラーメッセージ",
    "details": {
      "type": "エラーの種類",
      "message": "エラーメッセージ",
      "traceback": ["トレースバックの最後の10行"]
    },
    "path": "/",
    "timestamp": "2026-01-30T00:00:00"
  }
}
```

---

## ⚠️ 注意事項

- デバッグモードは開発環境でのみ使用してください
- 本番環境では`DEBUG=false`に設定してください
- エラーの詳細情報には機密情報が含まれる可能性があります

---

以上
