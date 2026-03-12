@echo off
cd /d "%~dp0"
echo ========================================
echo 医療データ異常検知MLOps - サーバー起動
echo ========================================
echo.
echo サーバーを起動しています...
echo ブラウザで http://localhost:8001/docs を開いてください
echo.
echo 停止するには Ctrl+C を押してください
echo ========================================
echo.

python api_server_enterprise.py

