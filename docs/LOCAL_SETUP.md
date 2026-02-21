# ローカル環境での実行（Docker不要）

**作成日**: 2026年1月29日  
**対象**: Dockerが使用できない環境、またはDockerを使わずに実行したい場合

---

## 📋 Dockerなしでの実行方法

Dockerは必須ではありません。以下の方法で実行可能です：

1. **ローカル環境で直接実行**（推奨）
2. **クラウド環境で実行**（AWS、Azure、GCP等）
3. **仮想環境で実行**（Vagrant、VirtualBox等）

---

## 🚀 ローカル環境での実行手順

### 前提条件

- Python 3.11以上
- Node.js 18以上（フロントエンド用）
- PostgreSQL（またはSQLite）
- Redis（オプション）

---

## 📦 バックエンドAPIの実行

### 1. Python仮想環境の作成

```bash
# プロジェクトディレクトリに移動
cd uep-v5-ultimate-enterprise-platform/backend

# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化（Windows）
venv\Scripts\activate

# 仮想環境の有効化（Linux/WSL）
source venv/bin/activate
```

### 2. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 3. 環境変数の設定

`.env`ファイルを作成：

```bash
# .env
DATABASE_URL=sqlite:///./uep_db.sqlite
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
```

### 4. バックエンドAPIの起動

```bash
# 直接実行
python main.py

# またはuvicornで実行
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**アクセス**: http://localhost:8000

---

## 🌐 フロントエンドの実行（オプション）

### 1. 依存パッケージのインストール

```bash
cd frontend
npm install
```

### 2. 開発サーバーの起動

```bash
npm run dev
```

**アクセス**: http://localhost:3000

---

## 🔧 各サービスのローカル実行

### Kong API Gateway（オプション）

KongはDockerなしでは実行が困難です。以下の代替案があります：

1. **Nginxを使用**（API Gatewayとして）
2. **Traefikを使用**（リバースプロキシとして）
3. **Kongなしで実行**（バックエンドAPIを直接使用）

### Prometheus（オプション）

```bash
# Prometheusをダウンロード・実行
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar xvfz prometheus-2.45.0.linux-amd64.tar.gz
cd prometheus-2.45.0.linux-amd64
./prometheus --config.file=prometheus.yml
```

### Grafana（オプション）

```bash
# Grafanaをダウンロード・実行
wget https://dl.grafana.com/oss/release/grafana-10.2.0.linux-amd64.tar.gz
tar -zxvf grafana-10.2.0.linux-amd64.tar.gz
cd grafana-10.2.0
./bin/grafana-server
```

---

## 📝 簡易起動スクリプト（Docker不要）

### start-local.sh

```bash
#!/bin/bash
# ローカル環境での起動スクリプト（Docker不要）

echo "=========================================="
echo "UEP v5.0 - ローカル環境での起動"
echo "=========================================="

# バックエンドAPIの起動
cd backend
if [ ! -d "venv" ]; then
    echo "仮想環境を作成中..."
    python -m venv venv
fi

echo "仮想環境を有効化中..."
source venv/bin/activate  # Linux/WSL
# venv\Scripts\activate  # Windows

echo "依存パッケージをインストール中..."
pip install -r requirements.txt

echo "バックエンドAPIを起動中..."
python main.py &
BACKEND_PID=$!

echo ""
echo "=========================================="
echo "起動完了"
echo "=========================================="
echo ""
echo "Backend API: http://localhost:8000"
echo ""
echo "停止: kill $BACKEND_PID"
echo ""
```

---

## ✅ Dockerなしでのメリット・デメリット

### メリット

- ✅ Dockerのインストールが不要
- ✅ 軽量で高速
- ✅ デバッグが容易
- ✅ 開発環境のセットアップが簡単

### デメリット

- ⚠️ 各サービスを個別にセットアップする必要がある
- ⚠️ 環境の再現性が低い
- ⚠️ 本番環境との差異が生じる可能性

---

## 🎯 推奨アプローチ

### 開発環境

- **Dockerなし**: ローカル環境で直接実行（開発・デバッグが容易）

### デモンストレーション環境

- **Docker使用**: 環境の再現性が高く、デモンストレーションに適している
- **Dockerなし**: 軽量で高速、セットアップが簡単

### 本番環境

- **Docker使用**: コンテナ化により、デプロイとスケーリングが容易

---

## 📋 まとめ

**Dockerは必須ではありません。**

- **開発**: Dockerなしでローカル実行可能
- **デモンストレーション**: Docker使用を推奨（環境の再現性）
- **本番**: Docker使用を推奨（コンテナ化のメリット）

必要に応じて、Dockerなしでの実行方法を選択できます。

---

以上
