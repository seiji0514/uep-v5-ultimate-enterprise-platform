# Phase 1: Docker - Multi-stage
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Frontend build
FROM node:20-alpine AS frontend
WORKDIR /frontend
# Node のヒープメモリ上限を増やし、Docker 内ビルドの OOM を防止
ENV NODE_OPTIONS="--max-old-space-size=4096"
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
ARG VITE_APP_TITLE=統合基盤プラットフォーム
ENV VITE_API_URL=
ENV VITE_APP_TITLE=$VITE_APP_TITLE
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
COPY --from=frontend /frontend/dist ./frontend_dist
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
