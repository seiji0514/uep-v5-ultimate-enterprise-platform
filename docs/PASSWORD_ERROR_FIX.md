# パスワードエラー修正ガイド

**作成日**: 2026年1月29日

---

## 🔧 問題

バックエンド起動時に以下のエラーが発生：

```
ValueError: password cannot be longer than 72 bytes
```

---

## ✅ 修正内容

### 1. パスワードハッシュ化の修正

`backend/auth/jwt_auth.py`の`get_password_hash()`メソッドを修正：

- bcryptの72バイト制限に対応
- パスワードが72バイトを超える場合は自動的に切り詰め
- エラーハンドリングを追加

### 2. デモユーザーの遅延初期化

`backend/auth/routes.py`の`DEMO_USERS`を遅延初期化に変更：

- モジュール読み込み時にパスワードハッシュ化を実行しない
- 初回アクセス時に初期化
- エラー時のフォールバック処理を追加

---

## 🚀 再起動方法

### 1. バックエンドを再起動

```cmd
cd backend
python main.py
```

または：

```cmd
start-backend.bat
```

### 2. 確認

以下のURLにアクセスして動作確認：

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ヘルスチェック**: http://localhost:8000/health

---

## 📝 デモユーザー

以下のユーザーでログインできます：

| ユーザー名 | パスワード | 権限 |
|-----------|-----------|------|
| admin | admin123 | admin |
| developer | dev123 | developer |
| viewer | view123 | viewer |

---

## ⚠️ 注意事項

- パスワードは72バイト（約72文字）以下にしてください
- 日本語パスワードも使用可能ですが、バイト数に注意してください
- 本番環境では、より強力なパスワードポリシーを実装してください

---

以上
