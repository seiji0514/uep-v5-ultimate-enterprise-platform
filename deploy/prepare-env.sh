#!/bin/bash
# デプロイ前準備スクリプト（Linux/macOS）
# SECRET_KEY 生成、.env テンプレート作成

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== UEP v5.0 デプロイ前準備 ==="

# SECRET_KEY 生成
if command -v openssl &> /dev/null; then
  SECRET_KEY=$(openssl rand -hex 32)
  echo "SECRET_KEY を生成しました"
else
  echo "警告: openssl がありません。SECRET_KEY を手動で設定してください"
  SECRET_KEY="CHANGE-ME-$(date +%s)"
fi

# backend/.env
if [ ! -f "$PROJECT_ROOT/backend/.env" ]; then
  cat > "$PROJECT_ROOT/backend/.env" << EOF
# 本番用（prepare-env.sh で生成）
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=$SECRET_KEY

# 以下を本番ドメインに変更してください
DATABASE_URL=postgresql://user:password@host:5432/uep_db
REDIS_URL=redis://:password@host:6379/0
CORS_ORIGINS=https://your-domain.com,https://industry.your-domain.com
LOG_LEVEL=WARNING
EOF
  echo "backend/.env を作成しました"
else
  echo "backend/.env は既に存在します。SECRET_KEY のみ更新する場合は手動で設定してください"
  echo "生成された SECRET_KEY: $SECRET_KEY"
fi

# 本番ユーザー永続化用（オプション）
mkdir -p "$PROJECT_ROOT/backend/data"
echo "backend/data/ を用意しました（PRODUCTION_USERS_FILE 用）"

echo ""
echo "=== 次のステップ ==="
echo "1. backend/.env の DATABASE_URL, CORS_ORIGINS を本番用に編集"
echo "2. frontend/.env.production を作成（REACT_APP_API_URL, REACT_APP_INDUSTRY_UNIFIED_URL）"
echo "3. industry_unified_platform/frontend/.env.production を作成（REACT_APP_INDUSTRY_API_URL）"
echo "4. deploy/nginx-ssl.conf.example を参考に nginx を設定"
echo "5. scripts/register_production_user.py で本番ユーザーを登録"
