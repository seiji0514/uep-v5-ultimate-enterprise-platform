@echo off
chcp 65001 >nul
REM 産業統合プラットフォーム - 個別起動（製造・IoT + 医療 + 金融 を1つに）

echo ==========================================
echo 産業統合プラットフォーム 起動
echo 製造・IoT + 医療・ヘルスケア + 金融・FinTech + 統合セキュリティ・防衛
echo ポート9010
echo ==========================================
echo.

cd /d "%~dp0"
cd ..\backend

if not exist "venv\Scripts\activate.bat" (
    echo エラー: 先に UEP の backend で venv を作成してください
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM 本番モードで起動（常に）
set ENVIRONMENT=production
set DEBUG=false

echo.
echo URL: http://localhost:9010
echo API: /api/v1/manufacturing, /api/v1/medical, /api/v1/fintech, /api/v1/security-defense-platform
echo Docs: http://localhost:9010/docs
echo.
echo 停止: Ctrl+C
echo ==========================================
echo.

python ..\industry_unified_platform\main.py

pause
