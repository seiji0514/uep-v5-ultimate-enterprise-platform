@echo off
chcp 65001 >nul
REM UEP v5.0 - 本番デプロイ用 バックエンド起動

echo ==========================================
echo UEP v5.0 - 本番用 バックエンド起動
echo ==========================================
echo.

cd /d "%~dp0"
cd ..

REM .env の確認
if not exist "backend\.env" (
    echo [注意] backend\.env がありません
    echo 本番デプロイ\本番デプロイ手順.md を参照して設定してください
    echo.
    pause
    exit /b 1
)

echo backend\.env を読み込みます
echo.

cd backend

REM 仮想環境
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

set ENVIRONMENT=production
set DEBUG=false

REM .env の UTF-8 読み込み対策（日本語コメント対応）
set PYTHONUTF8=1

echo 起動中: http://localhost:8080
echo 停止: Ctrl+C
echo ==========================================
echo.

python main.py

pause
