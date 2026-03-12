# 製造・IoTプラットフォーム

UEP v5.0・統合基盤とは**別の個別システム**です。単独で起動・運用します。

## 起動方法

1. **バックエンド**（ポート9002）
   ```bat
   start-backend.bat
   ```
   または
   ```powershell
   cd backend
   .\venv\Scripts\activate
   python ..\manufacturing_platform\main.py
   ```

2. **フロントエンド**（ポート3002）
   ```bat
   start-frontend.bat
   ```
   または
   ```powershell
   cd manufacturing_platform\frontend
   npm install
   npm start
   ```

## 機能

- 予知保全（Predictive Maintenance）
- センサーデータ取得（OPC-UA 連携）
- 異常検知

## API

- ベースURL: `http://localhost:9002`
- 認証: `/api/v1/auth/login`
- 製造API: `/api/v1/manufacturing/*`
