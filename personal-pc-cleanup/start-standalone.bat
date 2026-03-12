@echo off
chcp 65001 >nul
echo ==========================================
echo 個人用 PC 容量確保 - スタンドアロン
echo ==========================================
echo.

cd /d "%~dp0"

REM バックエンド
start "PC-Cleanup-API" cmd /k "cd /d %~dp0backend && pip install -r requirements.txt -q && uvicorn main:app --host 0.0.0.0 --port 5002"

REM フロントエンド起動待ち
timeout /t 4 /nobreak >nul

REM フロントエンド
start "PC-Cleanup-Front" cmd /k "cd /d %~dp0frontend && python -m http.server 3002"

echo.
echo 起動しました。
echo バックエンド: http://localhost:5002
echo フロントエンド: http://localhost:3002
echo API Docs: http://localhost:5002/docs
echo.
echo ブラウザで http://localhost:3002 を開いてください。
echo.
pause
