# 企業横断オペレーション基盤（Enterprise Operations Hub）

観測・タスク・リスクを一元管理する統合基盤。認証・RBAC・DB永続化・通知・CSV/Excelエクスポート対応。

## 注意事項

- **スキーマ変更**: スキーマバージョン不一致時は `eoh.db` を自動削除・再作成します（サンプルデータは自動投入）。
- **UEP連携**: UEPの `start-frontend.bat` / `start-frontend.ps1` で `REACT_APP_EOH_URL` を自動設定。手動起動時は `.env` に `REACT_APP_EOH_URL=http://localhost:3020` を追加してください。
- **初回起動**: バックエンドを先に起動してから、フロントエンドを起動してください。

## 起動方法

### バックエンド（ポート 9020）
```bash
cd enterprise_operations_hub
.\start-backend.bat
# または
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 9020 --reload
```

### フロントエンド（ポート 3020）
```bash
cd enterprise_operations_hub/frontend
npm install
npm start
```

### アクセス
- フロント: http://localhost:3020
- API: http://localhost:9020
- API Docs: http://localhost:9020/docs

## 本番運用

本番時は `ENVIRONMENT=production` と `EOH_SECRET_KEY` を設定してください。詳細は `docs/PRODUCTION_DEPLOYMENT.md` を参照。

- デモシード無効、API docs 無効、SECRET_KEY 必須

## ログイン（デモ）
| ユーザー | パスワード | ロール |
|----------|------------|--------|
| kaho0525 | 0525 | 管理者（全権限） |
| admin | admin123 | 管理者（全権限） |
| operator | op123 | オペレーター（書き込み・エクスポート） |
| viewer | view123 | 閲覧者（読み取り・エクスポート） |

## 機能

| 項目 | 内容 |
|------|------|
| 認証・RBAC | JWT認証、admin/operator/viewer ロール |
| DB永続化 | SQLite（デフォルト）、PostgreSQL（EOH_DATABASE_URL で指定） |
| 観測 | 設備異常・セキュリティ・顧客声など要対応の一覧 |
| タスク | 対応タスクの追加・着手・完了 |
| リスク | 属人化・不正リスクなど監視中のリスク |
| アラート | 閾値超過・期限間近などの通知、既読管理 |
| エクスポート | CSV/Excel（ダッシュボード・観測・タスク・リスク） |
| ドメイン | 製造・セキュリティ・顧客・人・組織・規制・財務・サプライチェーン・公共・小売・教育・法務・汎用 |

## 拡張機能（実装済み）

| 機能 | 内容 |
|------|------|
| UEP連携 | UEPダッシュボードからリンク、トークンSSO |
| 通知・メール | メール送信API（モック）、日次レポート |
| ダッシュボードカスタマイズ | 業種テンプレート（製造/医療/金融/SIer） |
| 検索・フィルタ | 観測・タスク・リスクの全文検索 |
| 外部API連携 | POST /api/v1/external/import でデータ取り込み |
| ワークフロー | タスクエスカレーション |
| 監査ログ | 操作履歴（admin権限で閲覧） |
| レポート定期実行 | POST /api/v1/reports/daily で日次レポート生成 |
| モバイル | PWA manifest、レスポンシブ |
| マルチテナント | tenant_id 対応（スキーマ準備済み） |
| AI分析 | GET /api/v1/ai/insights で簡易インサイト |
| BI連携 | GET /api/v1/bi/trends でトレンドデータ |
