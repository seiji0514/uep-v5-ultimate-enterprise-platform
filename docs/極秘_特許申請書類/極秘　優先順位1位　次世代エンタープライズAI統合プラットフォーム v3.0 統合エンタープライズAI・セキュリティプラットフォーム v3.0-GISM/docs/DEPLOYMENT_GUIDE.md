# デプロイメントガイド

**作成日**: 2025年12月7日  
**バージョン**: 8.0.0

---

## 📋 目次

1. [概要](#概要)
2. [前提条件](#前提条件)
3. [ローカル環境でのデプロイ](#ローカル環境でのデプロイ)
4. [Docker環境でのデプロイ](#docker環境でのデプロイ)
5. [本番環境でのデプロイ](#本番環境でのデプロイ)
6. [トラブルシューティング](#トラブルシューティング)

---

## 概要

次世代マルチモーダルAI統合プラットフォーム v8.0のデプロイメントガイドです。

---

## 前提条件

### **必要なソフトウェア**
- Python 3.13以上
- Docker Desktop（Docker環境を使用する場合）
- Git

### **必要なリソース**
- メモリ: 最低4GB（推奨8GB以上）
- ストレージ: 最低10GB
- CPU: 2コア以上（推奨4コア以上）

---

## ローカル環境でのデプロイ

### **1. リポジトリのクローン**

```bash
git clone <repository-url>
cd 次世代マルチモーダルAI統合プラットフォームv8.0
```

### **2. 仮想環境の作成**

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### **3. 依存関係のインストール**

```bash
pip install -r requirements.txt
```

### **4. アプリケーションの起動**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **5. 動作確認**

ブラウザで以下にアクセス：
- APIドキュメント: http://localhost:8000/docs
- ヘルスチェック: http://localhost:8000/health

---

## Docker環境でのデプロイ

### **1. Dockerイメージのビルド**

```bash
docker-compose build
```

### **2. コンテナの起動**

```bash
docker-compose up -d
```

### **3. ログの確認**

```bash
docker-compose logs -f
```

### **4. コンテナの停止**

```bash
docker-compose down
```

---

## 本番環境でのデプロイ

### **推奨構成**

- **Webサーバー**: Nginx
- **アプリケーションサーバー**: Gunicorn + Uvicorn
- **リバースプロキシ**: Nginx
- **データベース**: PostgreSQL（必要に応じて）
- **キャッシュ**: Redis（必要に応じて）

### **セキュリティ設定**

1. HTTPSの有効化
2. 認証・認可の実装
3. レート制限の実装
4. CORS設定の適切な設定

---

## トラブルシューティング

### **よくある問題**

1. **ポート8000が既に使用されている**
   - 別のポートを指定: `--port 8001`

2. **依存関係のインストールエラー**
   - Pythonバージョンを確認
   - 仮想環境を再作成

3. **Dockerビルドエラー**
   - Docker Desktopが起動しているか確認
   - キャッシュをクリア: `docker system prune -a`

---

**更新日**: 2025年12月7日

