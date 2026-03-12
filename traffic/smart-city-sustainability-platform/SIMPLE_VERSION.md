# 簡素化版システム

## 【概要】

最小限の機能のみを実装したシンプルなバージョンです。

## 【削除した機能】

- InfluxDB（時系列データベース）
- Kafka（メッセージキュー）
- Prometheus（監視）
- Grafana（可視化）
- 複雑な分析機能

## 【残した機能】

- PostgreSQL（またはSQLite）のみ
- 基本的なCRUD操作
- シンプルなダッシュボード
- ESGレポート生成（簡易版）

## 【必要なもの】

- Python 3.11以上
- Node.js 18以上
- PostgreSQL（またはSQLite使用で不要）

## 【セットアップ手順】

### 1. バックエンドのセットアップ

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic
```

### 2. データベースの設定（SQLite使用）

`backend/app/core/database.py` を以下のように変更：

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./smart_city.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 3. バックエンドの起動

```bash
# データベーステーブルの作成
python -c "from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)"

# サーバーの起動
uvicorn app.main:app --reload --port 8000
```

### 4. フロントエンドのセットアップ

```bash
cd frontend
npm install react react-dom react-router-dom axios
npm start
```

## 【簡素化された構成】

```
smart-city-sustainability-platform/
├── backend/
│   ├── app/
│   │   ├── main.py          # メインアプリ
│   │   ├── api/             # API（簡易版）
│   │   ├── models/          # データベースモデル
│   │   └── core/
│   │       └── database.py  # SQLite設定
│   └── requirements.txt    # 最小限の依存関係
└── frontend/
    ├── src/
    │   ├── App.tsx
    │   ├── pages/
    │   └── services/
    └── package.json
```

## 【APIエンドポイント（簡易版）】

- `GET /api/v1/sensors/` - センサー一覧
- `POST /api/v1/sensors/` - センサー作成
- `GET /api/v1/environment/data` - 環境データ取得
- `POST /api/v1/environment/data` - 環境データ作成
- `GET /api/v1/dashboard/overview` - ダッシュボード概要

## 【メリット】

✅ セットアップが簡単  
✅ 依存関係が少ない  
✅ 起動が速い  
✅ 理解しやすい  
✅ 開発・学習に最適  

## 【デメリット】

❌ 時系列データの高度な分析は不可  
❌ リアルタイム処理は不可  
❌ 大規模データには不向き  

---

**シンプルに始めたい方に最適です！**

