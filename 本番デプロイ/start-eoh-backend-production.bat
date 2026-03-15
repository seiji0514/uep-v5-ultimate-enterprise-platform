@echo off
chcp 65001 >nul
REM 企業横断オペレーション基盤（EOH）- 本番用 バックエンド起動

echo ==========================================
echo 企業横断オペレーション基盤（EOH）- 本番用 バックエンド
echo ==========================================
echo.

cd /d "%~dp0"
cd ..

cd enterprise_operations_hub\backend

REM .env の確認
if not exist ".env" (
    if exist ".env.production.example" (
        echo [注意] .env がありません。.env.production.example をコピーして .env を作成し、
        echo EOH_SECRET_KEY を設定してください（openssl rand -hex 32 で生成）
    ) else (
        echo [注意] .env がありません
    )
    echo docs\PRODUCTION_DEPLOYMENT.md を参照してください
    echo.
    pause
    exit /b 1
)

set ENVIRONMENT=production
set PYTHONUTF8=1

echo 起動中: http://localhost:9020
echo 停止: Ctrl+C
echo ==========================================
echo.

python -m uvicorn main:app --host 0.0.0.0 --port 9020

pause
