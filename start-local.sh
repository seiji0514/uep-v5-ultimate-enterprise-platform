#!/bin/bash
# UEP v5.0 - ローカル環境での起動スクリプト（Docker不要）

echo "=========================================="
echo "UEP v5.0 - ローカル環境での起動"
echo "Docker不要"
echo "=========================================="

# プロジェクトディレクトリに移動
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Pythonの確認
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "エラー: Pythonがインストールされていません"
    exit 1
fi

# バックエンドAPIの起動
echo ""
echo "1. バックエンドAPIのセットアップ..."
cd backend

# 仮想環境の作成
if [ ! -d "venv" ]; then
    echo "   仮想環境を作成中..."
    python3 -m venv venv || python -m venv venv
fi

# 仮想環境の有効化
echo "   仮想環境を有効化中..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# 依存パッケージのインストール
echo "   依存パッケージをインストール中..."
pip install --upgrade pip
pip install -r requirements.txt

# 環境変数の設定（.envファイルがない場合）
if [ ! -f ".env" ]; then
    echo "   .envファイルを作成中..."
    cat > .env << EOF
DATABASE_URL=sqlite:///./uep_db.sqlite
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || python -c "import secrets; print(secrets.token_hex(32))")
EOF
fi

# バックエンドAPIの起動
echo ""
echo "2. バックエンドAPIを起動中..."
echo "   URL: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "   停止: Ctrl+C"
echo ""

python main.py
