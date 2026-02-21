# E2E テスト (Playwright)

## 前提条件

- **バックエンド**が起動していること（`start-backend.bat` → http://localhost:8000 または 8001）
- **フロントエンド**の `.env` がバックエンドのポートと一致していること（例: `REACT_APP_API_URL=http://localhost:8001`）

## セットアップ

```bash
cd e2e
npm install
npx playwright install chromium
```

## 実行

```bash
# Chromium のみ（推奨・高速）
npx playwright test --project=chromium

# 全ブラウザ
npm test
```

## テスト内容

- **login.spec.ts**: ログインフォーム表示、ログイン成功、未認証時のリダイレクト
- **chaos.spec.ts**: Chaos ページ遷移、遅延シナリオ UI 表示（ログイン済み）
