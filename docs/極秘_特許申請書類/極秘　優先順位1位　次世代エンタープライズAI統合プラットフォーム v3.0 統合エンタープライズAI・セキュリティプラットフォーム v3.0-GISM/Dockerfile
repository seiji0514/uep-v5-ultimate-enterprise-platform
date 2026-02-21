FROM python:3.13-slim

WORKDIR /app

# システム依存関係のインストール
# 非インタラクティブモードを設定
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    default-jdk \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Java環境変数設定（Spark用）
# default-jdkは通常java-11ですが、SparkはJava 8+をサポート
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$PATH:$JAVA_HOME/bin

# Python依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# torchを個別にインストール（オプショナル、必要に応じて有効化）
# RUN pip install --no-cache-dir torch>=2.6.0 torchvision>=0.21.0 --index-url https://download.pytorch.org/whl/cpu

# アプリケーションコピー
COPY . .

# ポート公開
EXPOSE 8000

# アプリケーション起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

