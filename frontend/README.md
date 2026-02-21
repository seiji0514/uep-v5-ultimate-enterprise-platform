# UEP v5.0 - フロントエンド

次世代エンタープライズ統合プラットフォーム v5.0 のフロントエンドアプリケーション

## 技術スタック

- **React** 19.2.4
- **TypeScript** 4.9.5
- **Material-UI** 5.15.0
- **React Router** 6.21.1
- **Axios** 1.6.2

## セットアップ

### 依存関係のインストール

```bash
npm install
```

### 環境変数の設定

`.env`ファイルに以下を設定：

```
REACT_APP_API_URL=http://localhost:8000
```

## 起動方法

### 開発サーバーの起動

```bash
npm start
```

または、プロジェクトルートから：

```bash
start-frontend.bat
```

フロントエンドは `http://localhost:3000` で起動します。

## 認証情報

デモユーザー：
- **管理者**: `kaho0525` / `kaho052514`
- **開発者**: `developer` / `dev123`
- **閲覧者**: `viewer` / `view123`

## プロジェクト構造

```
frontend/
├── src/
│   ├── api/              # APIクライアント
│   │   ├── client.ts    # Axios設定
│   │   └── auth.ts       # 認証API
│   ├── components/       # Reactコンポーネント
│   │   ├── Auth/        # 認証関連
│   │   ├── Dashboard/   # ダッシュボード
│   │   └── Layout/      # レイアウト
│   ├── contexts/         # React Context
│   │   └── AuthContext.tsx
│   ├── App.tsx          # メインアプリケーション
│   └── index.tsx        # エントリーポイント
├── public/              # 静的ファイル
└── package.json         # 依存関係
```

## 機能

- ✅ 認証機能（ログイン、トークン管理）
- ✅ ダッシュボード
- ✅ レスポンシブレイアウト
- ✅ Material-UIによるモダンなUI
- ✅ 保護されたルート
- 🔄 各システムのUI（実装予定）

## ビルド

本番環境用のビルド：

```bash
npm run build
```

ビルドされたファイルは `build/` ディレクトリに生成されます。
