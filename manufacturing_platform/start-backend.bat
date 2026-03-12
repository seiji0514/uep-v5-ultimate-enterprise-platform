@echo off
chcp 65001 >nul
REM 製造・IoTプラットフォーム - 個別起動（UEP v5.0 とは別）

echo ==========================================
echo 製造・IoTプラットフォーム 起動
echo 個別システム - ポート9002
echo ==========================================
echo.

cd /d "%~dp0"

REM UEP の backend を利用（venv, requirements）
cd ..\backend

if not exist "venv\Scripts\activate.bat" (
    echo エラー: 先に UEP の backend で venv を作成してください
    echo cd ..\backend
    echo python -m venv venv
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo.
echo URL: http://localhost:9002
echo API: http://localhost:9002/api/v1/manufacturing
echo Docs: http://localhost:9002/docs
echo.
echo 停止: Ctrl+C
echo ==========================================
echo.

python ..\manufacturing_platform\main.py

pause
