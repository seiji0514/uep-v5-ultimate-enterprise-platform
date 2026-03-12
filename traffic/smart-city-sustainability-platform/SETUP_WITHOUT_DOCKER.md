# Dockerなしで実行する方法

## 【概要】

Dockerを使わずに、ローカルPCで直接実行する方法です。

## 【方法1: 最小構成（推奨）】

PostgreSQLのみを使用し、InfluxDBとKafkaはオプションにします。

### 必要なもの

1. **Python 3.13**（または3.11以上）
2. **Node.js 20**（または18以上）
3. **PostgreSQL 15**（または12以上）
4. **npm**（Node.jsに含まれる）

### セットアップ手順

#### 1. PostgreSQLのインストール

**Windows:**
- [PostgreSQL公式サイト](https://www.postgresql.org/download/windows/)からインストーラーをダウンロード

**Mac:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### 2. データベースの作成

```bash
# PostgreSQLに接続
psql -U postgres

# データベースを作成
CREATE DATABASE smart_city_sustainability;

# ユーザーを作成（必要に応じて）
CREATE USER smart_city_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE smart_city_sustainability TO smart_city_user;

# 終了
\q
```

#### 3. バックエンドのセットアップ

```bash
cd backend

# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
# .envファイルを作成（または環境変数を設定）
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=smart_city_sustainability
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

#### 4. バックエンドの起動

```bash
# データベーステーブルの作成
python -c "from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)"

# サーバーの起動
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 5. フロントエンドのセットアップ

```bash
cd frontend

# 依存関係のインストール
npm install

# 環境変数の設定
# .envファイルを作成
REACT_APP_API_URL=http://localhost:8000
```

#### 6. フロントエンドの起動

```bash
npm start
```

### アクセス

- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:8000
- **APIドキュメント**: http://localhost:8000/docs

---

## 【方法2: 簡易版（SQLite使用）】

PostgreSQLも不要で、SQLiteを使用する軽量版です。

### 必要なもの

1. **Python 3.13**（または3.11以上）
2. **Node.js 20**（または18以上）
3. **npm**（Node.jsに含まれる）

### セットアップ手順

#### 1. バックエンドの設定変更

`backend/app/core/database.py` を以下のように変更：

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# SQLiteを使用
DATABASE_URL = "sqlite:///./smart_city.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite用
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

#### 2. バックエンドのセットアップ

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

#### 3. バックエンドの起動

```bash
# データベーステーブルの作成
python -c "from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)"

# サーバーの起動
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 4. フロントエンドのセットアップ

```bash
cd frontend
npm install
npm start
```

### 注意事項

- **InfluxDB機能は使用不可**（時系列データはSQLiteに保存）
- **Kafka機能は使用不可**（メッセージキューは無効化）
- **本番環境には不向き**（開発・テスト用途のみ）

---

## 【方法3: クラウドサービスを利用】

外部のクラウドサービス（無料枠）を利用する方法です。

### 利用可能なサービス

1. **PostgreSQL**: [Supabase](https://supabase.com/)（無料枠あり）
2. **InfluxDB**: [InfluxDB Cloud](https://www.influxdata.com/products/influxdb-cloud/)（無料枠あり）
3. **Kafka**: [Confluent Cloud](https://www.confluent.io/confluent-cloud/)（無料トライアル）

### セットアップ

各サービスの接続情報を環境変数に設定：

```bash
# .envファイル
POSTGRES_HOST=your-supabase-host
POSTGRES_USER=your-user
POSTGRES_PASSWORD=your-password
POSTGRES_DB=your-database

INFLUXDB_URL=https://your-influxdb-url
INFLUXDB_TOKEN=your-token
```

---

## 【推奨構成】

### 開発・テスト用途
- **方法2（SQLite使用）**: 最も簡単、すぐに始められる

### 本格的な開発
- **方法1（PostgreSQL使用）**: 本番環境に近い構成

### 本番環境
- **Docker Compose使用**: すべてのサービスを統合管理

---

## 【トラブルシューティング】

### PostgreSQL接続エラー

```bash
# PostgreSQLが起動しているか確認
# Windows:
sc query postgresql-x64-15
# Mac/Linux:
sudo systemctl status postgresql

# 接続テスト
psql -U postgres -h localhost
```

### ポートが使用中

```bash
# ポート8000が使用中の場合
# Windows:
netstat -ano | findstr :8000
# Mac/Linux:
lsof -i :8000

# 別のポートを使用
uvicorn app.main:app --reload --port 8001
```

---

**ご質問・ご要望がございましたら、お気軽にお申し付けください。**

