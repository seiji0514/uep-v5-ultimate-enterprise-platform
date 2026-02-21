# CSPソースマップエラー修正ガイド

**作成日**: 2026年1月30日

---

## 問題の症状

Swagger UI (`/docs`) で以下のCSPエラーが表示される：

```
Connecting to 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js.map' violates the following Content Security Policy directive: "connect-src 'self'". The request has been blocked.
```

---

## 原因

Content Security Policy (CSP) の `connect-src` ディレクティブが `'self'` のみに設定されているため、Swagger UIのソースマップファイル（`.map`ファイル）を外部CDN（`cdn.jsdelivr.net`）から読み込むことができません。

---

## 修正内容

`backend/core/security.py` の `SecurityHeadersMiddleware` を修正：

**修正前:**
```python
"connect-src 'self'"
```

**修正後:**
```python
"connect-src 'self' https://cdn.jsdelivr.net"
```

これにより、Swagger UIのソースマップファイルの読み込みが許可されます。

---

## 修正手順

### ステップ1: バックエンドを再起動

```cmd
# バックエンドを停止（Ctrl+C）
# その後、再起動
start-backend.bat
```

### ステップ2: Swagger UIを確認

1. `http://localhost:8000/docs` にアクセス
2. ブラウザの開発者ツール（F12）を開く
3. ConsoleタブでCSPエラーが解消されているか確認

---

## 注意事項

- ソースマップファイルは開発時にのみ使用されます
- 本番環境では通常、ソースマップファイルは配布されません
- この修正は開発環境でのみ影響があります

---

## セキュリティへの影響

- `cdn.jsdelivr.net` は信頼できるCDNです
- Swagger UIのソースマップファイルのみが許可されます
- 他の外部リソースへの接続は引き続きブロックされます

---

以上
