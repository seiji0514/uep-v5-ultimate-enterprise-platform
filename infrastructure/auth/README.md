# 統合認証・認可システム

**作成日**: 2026年1月29日  
**Phase**: 1.2

---

## 📋 概要

UEP v5.0の統合認証・認可システムは、以下の機能を提供します：

- **JWT認証**: トークンベースの認証
- **OAuth2/OIDC**: 標準的なOAuth2/OIDCフロー
- **RBAC**: ロールベースアクセス制御
- **ABAC**: 属性ベースアクセス制御

---

## 🏗️ アーキテクチャ

```
backend/auth/
├── __init__.py          # モジュール初期化
├── jwt_auth.py          # JWT認証実装
├── oauth2.py            # OAuth2/OIDC実装
├── rbac.py              # RBAC実装
├── abac.py              # ABAC実装
├── models.py            # データモデル
└── routes.py            # APIエンドポイント
```

---

## 🔐 認証方式

### JWT認証

- アクセストークンの生成・検証
- パスワードハッシュ化（bcrypt）
- トークン有効期限管理

### OAuth2/OIDC

- 認証コードフロー
- トークン交換
- ユーザー情報取得

---

## 👥 ロールとパーミッション

### ロール

- **admin**: 管理者（全権限）
- **developer**: 開発者（MLOps/AI管理）
- **operator**: 運用者（インフラ管理）
- **viewer**: 閲覧者（読み取りのみ）
- **user**: 一般ユーザー（自分のリソースのみ）

### パーミッション

- `read`: 読み取り
- `write`: 書き込み
- `delete`: 削除
- `admin`: 管理権限
- `manage_users`: ユーザー管理
- `manage_roles`: ロール管理
- `manage_mlops`: MLOps管理
- `manage_ai`: AI管理
- `monitor`: 監視
- `manage_infrastructure`: インフラ管理
- `write_own`: 自分のリソースのみ書き込み

---

## 📝 APIエンドポイント

### 認証

- `POST /api/v1/auth/register` - ユーザー登録
- `POST /api/v1/auth/login` - ログイン（JWTトークン発行）
- `POST /api/v1/auth/token` - OAuth2互換トークンエンドポイント
- `GET /api/v1/auth/me` - 現在のユーザー情報取得
- `POST /api/v1/auth/change-password` - パスワード変更

### 保護されたエンドポイント

- `GET /api/v1/services` - サービス一覧（認証必須）
- `GET /api/v1/gateway/routes` - ルート一覧（read権限必須）
- `GET /api/v1/admin/users` - ユーザー一覧（adminロール必須）

---

## 🚀 使用方法

### 1. ユーザー登録

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 2. ログイン

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

レスポンスから `access_token` を取得します。

### 3. 認証が必要なAPIを呼び出す

```bash
curl -X GET "http://localhost:8000/api/v1/services" \
  -H "Authorization: Bearer <access_token>"
```

---

## 🔒 デモユーザー

以下のデモユーザーが事前に登録されています：

| ユーザー名 | パスワード | ロール    | パーミッション                       |
| ---------- | ---------- | --------- | ------------------------------------ |
| admin      | admin123   | admin     | 全権限                               |
| developer  | dev123     | developer | read, write, manage_mlops, manage_ai |
| viewer     | view123    | viewer    | read                                 |

---

## 📚 参考資料

- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT.io](https://jwt.io/)
- [OAuth 2.0](https://oauth.net/2/)
- [OpenID Connect](https://openid.net/connect/)

---

以上
