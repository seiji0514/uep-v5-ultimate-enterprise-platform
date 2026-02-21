@echo off
chcp 65001 >nul
REM UEP v5.0 - バックエンドAPI起動（ポート8001使用・8000が使用中の場合の代替）

echo ==========================================
echo UEP v5.0 - バックエンドAPI起動（ポート8001）
echo ==========================================
echo.
echo ※ ポート8000が使用中のため、8001で起動します
echo    URL: http://localhost:8001
echo    API Docs: http://localhost:8001/docs
echo.

cd /d "%~dp0"
cd backend

call venv\Scripts\activate.bat 2>nul
if errorlevel 1 (
    echo 仮想環境が見つかりません。先に start-backend.bat を1回実行してください。
    pause
    exit /b 1
)

set PORT=8001
python main.py

pause
