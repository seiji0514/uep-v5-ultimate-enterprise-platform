# 医療データ異常検知MLOps - Dockerfile
# 企業レベル本番環境対応

FROM python:3.11-slim

# 作業ディレクトリ
WORKDIR /app

# 環境変数
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# システムパッケージのインストール
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 依存関係ファイルのコピー
COPY requirements.txt .

# Python依存関係のインストール
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# アプリケーションファイルのコピー
COPY . .

# ログディレクトリの作成
RUN mkdir -p logs

# 非rootユーザーの作成
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8001/health')"

# ポート公開
EXPOSE 8001

# アプリケーション起動
CMD ["python", "api_server_enterprise.py"]

