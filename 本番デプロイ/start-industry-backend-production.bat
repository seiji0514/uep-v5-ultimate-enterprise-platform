@echo off
chcp 65001 >nul
REM 産業統合プラットフォーム - 本番用 バックエンド起動

echo ==========================================
echo 産業統合プラットフォーム - 本番用 バックエンド
echo 製造・IoT + 医療 + 金融 + 統合セキュリティ
echo ==========================================
echo.

cd /d "%~dp0"
cd ..

REM UEP backend の venv を使用
cd backend
if not exist "venv\Scripts\activate.bat" (
    echo [Error] backend\venv がありません。先に UEP の backend で venv を作成してください
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

set ENVIRONMENT=production
set DEBUG=false
set INDUSTRY_UNIFIED_PORT=9010
set INDUSTRY_UNIFIED_HOST=0.0.0.0
set PYTHONUTF8=1

echo 起動中: http://localhost:9010
echo 停止: Ctrl+C
echo ==========================================
echo.

python ..\industry_unified_platform\main.py

pause
