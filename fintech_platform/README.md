# 金融・FinTechプラットフォーム

UEP v5.0・統合基盤とは**別の個別システム**です。単独で起動・運用します。

## 起動方法

1. **バックエンド**（ポート9004）
   ```bat
   start-backend.bat
   ```

2. **フロントエンド**（ポート3004）
   ```bat
   start-frontend.bat
   ```

## 機能

- 決済一覧
- リスクスコア
- 取引監視
- ストレステスト（規制対応）

## API

- ベースURL: `http://localhost:9004`
- 認証: `/api/v1/auth/login`
- 金融API: `/api/v1/fintech/*`
