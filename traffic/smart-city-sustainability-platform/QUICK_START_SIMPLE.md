# クイックスタート（簡素化版）

## 【概要】

最小限の機能のみを実装したシンプルなバージョンです。  
**Docker不要、PostgreSQL不要、SQLiteのみで動作します。**

## 【必要なもの】

- Python 3.11以上
- Node.js 18以上
- それだけ！

## 【セットアップ手順（5分で完了）】

### 1. バックエンドのセットアップ

```bash
cd backend

# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 最小限の依存関係のインストール
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv

# データベースの初期化（SQLite使用）
python -c "from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

### 2. バックエンドの起動

```bash
# 簡易版メインファイルを使用
python app/main_simple.py

# または
uvicorn app.main_simple:app --reload --port 8000
```

### 3. フロントエンドのセットアップ（別ターミナル）

```bash
cd frontend

# 最小限の依存関係のインストール
npm install react react-dom react-router-dom axios vite @vitejs/plugin-react

# 開発サーバーの起動
npm run dev
```

### 4. アクセス

- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:8000
- **APIドキュメント**: http://localhost:8000/docs

## 【簡素化された機能】

✅ 基本的なCRUD操作  
✅ シンプルなダッシュボード  
✅ SQLiteデータベース（ファイルベース）  
✅ 最小限の依存関係  

## 【含まれていない機能】

❌ InfluxDB（時系列データベース）  
❌ Kafka（メッセージキュー）  
❌ Prometheus（監視）  
❌ Grafana（可視化）  
❌ 複雑な分析機能  

## 【ファイル構成】

```
backend/
├── app/
│   ├── main_simple.py      # 簡易版メイン（これを使用）
│   ├── main.py             # フル版メイン（使用しない）
│   └── core/
│       └── database.py     # SQLite設定
└── requirements_simple.txt # 最小限の依存関係

frontend/
├── src/
│   ├── App.tsx
│   └── services/
└── package_simple.json     # 最小限の依存関係
```

## 【次のステップ】

1. 基本的な動作確認
2. 必要に応じて機能を追加
3. フル版に移行（必要に応じて）

---

**シンプルに始めたい方に最適です！**

