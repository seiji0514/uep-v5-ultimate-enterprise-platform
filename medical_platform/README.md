# 医療・ヘルスケアプラットフォーム

UEP v5.0・統合基盤とは**別の個別システム**です。単独で起動・運用します。

## 起動方法

1. **バックエンド**（ポート9003）
   ```bat
   start-backend.bat
   ```
   または
   ```powershell
   cd backend
   .\venv\Scripts\activate
   python ..\medical_platform\main.py
   ```

2. **フロントエンド**（ポート3003）
   ```bat
   start-frontend.bat
   ```
   または
   ```powershell
   cd medical_platform\frontend
   npm install
   npm start
   ```

## 機能

- AI診断支援
- 音声応答（問診・ナースコール）
- 異常検知（バイタル・検査値）
- プラットフォーム統計

## API

- ベースURL: `http://localhost:9003`
- 認証: `/api/v1/auth/login`
- 医療API: `/api/v1/medical/*`
