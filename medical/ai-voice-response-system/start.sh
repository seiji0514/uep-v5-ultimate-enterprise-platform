#!/bin/bash

echo "========================================"
echo "AI自動音声応答システム 起動スクリプト"
echo "========================================"
echo ""

cd "$(dirname "$0")"

echo "[1/4] Pythonのバージョン確認..."
python3 --version || python --version
if [ $? -ne 0 ]; then
    echo "エラー: Pythonがインストールされていません"
    echo "Python 3.8以上をインストールしてください"
    exit 1
fi

echo ""
echo "[2/4] 依存関係の確認..."
python3 -m pip list | grep -q fastapi || python -m pip list | grep -q fastapi
if [ $? -ne 0 ]; then
    echo "依存関係をインストール中..."
    echo "初回インストールには時間がかかります..."
    python3 -m pip install -r requirements.txt || python -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "エラー: 依存関係のインストールに失敗しました"
        echo "手動でインストールしてください: pip install -r requirements.txt"
        exit 1
    fi
    echo "依存関係のインストールが完了しました"
else
    echo "依存関係は既にインストールされています"
fi

echo ""
echo "[3/4] 設定ファイルの確認..."
if [ ! -f ".env" ]; then
    echo ".envファイルが見つかりません"
    echo "オプション: .envファイルを作成してOpenAI API Keyを設定できます"
    echo "ローカルモデルのみ使用する場合は設定不要です"
fi

echo ""
echo "[4/4] バックエンドサーバーを起動中..."
echo ""
echo "========================================"
echo "サーバー起動完了後、ブラウザで以下を開いてください:"
echo "http://localhost:8000"
echo "========================================"
echo ""
echo "停止するには Ctrl+C を押してください"
echo ""

cd backend
python3 main.py || python main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "エラーが発生しました"
    echo "ログを確認してください"
    exit 1
fi
