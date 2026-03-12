# 個人会計 - スタンドアロン版

UEP v5.0 から独立した、個人用会計システム（freee・マネーフォワード風）。

## 機能

### 会計
- 経費・売上の登録・一覧・削除
- 経費判定（カテゴリ別に経費/経費外を自動判定）
- ダッシュボード（今月・今年累計）
- カテゴリ一覧
- **領収書OCR** … 画像アップロードで日付・金額・店名を自動抽出し、経費候補として登録
- **領収書の保管** … 経費に領収書画像を紐付け保存。一覧表示・ダウンロード対応（税務上の7年保存に活用）
- **確定申告書** … 収支内訳書風のHTMLを生成（印刷でPDF化可能）
- **請求書PDF** … 請求書をPDFで出力

### フリーランス業務
- **タスク管理** … 案件・タスクの登録、納期、進捗（未着手/進行中/完了）
- **スケジュール管理** … カレンダー風予定の登録・一覧
- **契約書** … 業務委託契約の登録、PDF出力
- **ファイル共有** … 納品物・資料のアップロード・ダウンロード

## 必要環境

- Python 3.10+
- ブラウザ（Chrome, Edge, Firefox 等）
- **領収書OCR 利用時**: [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki) のインストールと PATH 設定（日本語は `jpn` データを追加）

## 起動方法

### Windows

```cmd
start-standalone.bat
```

または手動で:

```cmd
REM ターミナル1: バックエンド
cd standalone-personal-accounting\backend
pip install -r requirements.txt
python main.py

REM ターミナル2: フロントエンド
cd standalone-personal-accounting\frontend
python -m http.server 3001
```

- バックエンド: http://localhost:5000
- フロントエンド: http://localhost:3001（UEP v5.0 が 3000 を使用するため）
- API ドキュメント: http://localhost:5000/docs

### Linux / macOS

```bash
# ターミナル1
cd standalone-personal-accounting/backend
pip install -r requirements.txt
python main.py

# ターミナル2
cd standalone-personal-accounting/frontend
python3 -m http.server 3001
```

ブラウザで http://localhost:3001 を開く。

## 練習用と本番用の切り替え

| モード | 起動方法 | ポート | データファイル |
|--------|----------|--------|----------------|
| **本番** | `start-standalone.bat` | バックエンド:5000, フロント:3001 | `personal_accounting.json`, `receipts/` |
| **練習** | `start-standalone-practice.bat` | バックエンド:5001, フロント:3010 | `personal_accounting_practice.json`, `receipts_practice/` |

練習モードでは架空データで操作を試せます。本番データとは完全に分離され、**別ポートで同時起動可能**です。画面上に「練習モード」「本番」のバッジで表示されます。

- 本番: http://localhost:3001
- 練習: http://localhost:3010

**運用の目安**: 参画確定までは練習モードで操作に慣れ、確定後は本番モードで実データを管理してください。

手動起動で練習モードにする場合:
```cmd
set PERSONAL_ACCOUNTING_MODE=practice
set PERSONAL_ACCOUNTING_PORT=5001
python main.py
```

## データ保存

- 本番: `backend/data/personal_accounting.json`, `backend/data/receipts/`
- 練習: `backend/data/personal_accounting_practice.json`, `backend/data/receipts_practice/`
- バックエンドと同じディレクトリで実行してください

## UEP v5.0 との違い

| 項目 | UEP版 | スタンドアロン版 |
|------|-------|------------------|
| 認証 | 必要（JWT） | 不要 |
| 依存 | UEP 全体 | なし（FastAPI のみ） |
| フロント | React (UEP内) | 単一HTML |
| 起動 | start-backend.bat + npm start | 本READMEの手順 |
