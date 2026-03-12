# ローカル開発環境ガイド（サーバー不要）

## 【概要】

このシステムは**専用サーバー不要**で、ローカルPC（Windows、Mac、Linux）で実行できます。

## 【必要なもの】

1. **Docker Desktop**（またはDocker + Docker Compose）
   - Windows/Mac: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Linux: Docker + Docker Compose
2. **約4GB以上の空きメモリ**（推奨）
3. **インターネット接続**（初回ダウンロード時のみ）

## 【実行方法】

### 1. Docker Desktopのインストール

- Windows/Mac: Docker Desktopをダウンロードしてインストール
- Linux: `sudo apt-get install docker docker-compose`（Ubuntu/Debianの場合）

### 2. システムの起動

```bash
cd smart-city-sustainability-platform
docker-compose up -d
```

これだけで、すべてのサービス（バックエンド、フロントエンド、データベース等）がローカルPC上で起動します。

### 3. アクセス

- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:8000
- **APIドキュメント**: http://localhost:8000/docs

## 【サーバーが必要な場合】

以下の場合のみ、サーバー（クラウド等）が必要です：

1. **外部に公開したい場合**
   - インターネット経由でアクセス可能にしたい
   - 複数のユーザーがアクセスする

2. **本番環境として運用する場合**
   - 24時間365日稼働させる
   - 大規模なデータ処理が必要

## 【サーバー不要でできること】

✅ ローカルでの開発・テスト  
✅ デモ・プレゼンテーション  
✅ 個人プロジェクトの運用  
✅ 学習・研究用途  
✅ 小規模なチーム内での利用  

## 【Dockerなしで実行する場合（オプション）】

Dockerを使わずに、直接実行することも可能です：

### バックエンドのみ

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### フロントエンドのみ

```bash
cd frontend
npm install
npm start
```

ただし、この場合はPostgreSQL、InfluxDB、Kafka等を別途インストール・設定する必要があります。

## 【まとめ】

- **開発・テスト用途**: サーバー不要（ローカルPCで実行可能）
- **本番環境・外部公開**: サーバー必要（クラウドサービス推奨）

---

**ご質問・ご要望がございましたら、お気軽にお申し付けください。**

