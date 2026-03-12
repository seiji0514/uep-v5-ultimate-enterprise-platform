@echo off
chcp 65001 >nul
REM 医療・ヘルスケアプラットフォーム - 個別起動（UEP v5.0 とは別）

echo ==========================================
echo 医療・ヘルスケアプラットフォーム 起動
echo 個別システム - ポート9003
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
echo URL: http://localhost:9003
echo API: http://localhost:9003/api/v1/medical
echo Docs: http://localhost:9003/docs
echo.
echo 停止: Ctrl+C
echo ==========================================
echo.

python ..\medical_platform\main.py

pause
