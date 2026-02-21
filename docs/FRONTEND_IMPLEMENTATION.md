# フロントエンド実装ガイド

**作成日**: 2026年1月30日

---

## 概要

UEP v5.0のフロントエンドは、React + TypeScript + Material-UIで実装されたエンタープライズレベルのWebアプリケーションです。

---

## 実装済み機能

### ✅ 基本機能

1. **認証機能**
   - ログインページ
   - JWTトークン管理
   - 認証コンテキスト（React Context）
   - 保護されたルート

2. **レイアウト**
   - レスポンシブサイドバー
   - ヘッダー（ユーザーメニュー付き）
   - Material-UIテーマ

3. **ダッシュボード**
   - メインダッシュボードページ
   - システムカード表示
   - ナビゲーション

4. **APIクライアント**
   - AxiosベースのAPIクライアント
   - 認証トークンの自動付与
   - エラーハンドリング

---

## プロジェクト構造

```
frontend/
├── src/
│   ├── api/                    # APIクライアント
│   │   ├── client.ts          # Axios設定とインターセプター
│   │   └── auth.ts            # 認証API
│   ├── components/            # Reactコンポーネント
│   │   ├── Auth/              # 認証関連
│   │   │   └── LoginPage.tsx  # ログインページ
│   │   ├── Dashboard/        # ダッシュボード
│   │   │   └── DashboardPage.tsx
│   │   ├── Layout/            # レイアウト
│   │   │   └── MainLayout.tsx # メインレイアウト
│   │   └── ProtectedRoute.tsx # 保護されたルート
│   ├── contexts/              # React Context
│   │   └── AuthContext.tsx    # 認証コンテキスト
│   ├── App.tsx                # メインアプリケーション
│   ├── index.tsx              # エントリーポイント
│   └── index.css              # グローバルスタイル
├── public/                     # 静的ファイル
├── .env                       # 環境変数
└── package.json               # 依存関係
```

---

## 起動手順

### 1. 依存関係のインストール

```cmd
cd frontend
npm install
```

### 2. フロントエンドの起動

```cmd
npm start
```

または、プロジェクトルートから：

```cmd
start-frontend.bat
```

### 3. アクセス

ブラウザで `http://localhost:3000` にアクセス

---

## 認証情報

デモユーザー：
- **管理者**: `kaho0525` / `kaho052514`
- **開発者**: `developer` / `dev123`
- **閲覧者**: `viewer` / `view123`

---

## 実装予定機能

### 🔄 各システムのUIコンポーネント

- MLOpsダッシュボード
- 生成AIインターフェース
- セキュリティコマンドセンター
- クラウドインフラ管理
- IDOPダッシュボード
- AI支援開発ツール

---

## 技術スタック

- **React** 19.2.4
- **TypeScript** 4.9.5
- **Material-UI** 5.15.0
- **React Router** 6.21.1
- **Axios** 1.6.2

---

## 環境変数

`.env`ファイルで設定：

```
REACT_APP_API_URL=http://localhost:8000
```

---

## トラブルシューティング

### 依存関係のインストールエラー

```cmd
cd frontend
rmdir /s /q node_modules
del package-lock.json
npm install
```

### ポート3000が使用中

別のポートで起動：

```cmd
set PORT=3001
npm start
```

---

以上
