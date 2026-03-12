@echo off
chcp 65001 >nul
REM 製造・IoTプラットフォーム フロントエンド起動（ポート3002）

echo ==========================================
echo 製造・IoTプラットフォーム フロントエンド
echo ポート3002
echo ==========================================
echo.

cd /d "%~dp0frontend"

if not exist "node_modules" (
    echo npm install を実行します...
    call npm install
)

echo.
echo URL: http://localhost:3002
echo バックエンド: http://localhost:9002
echo ==========================================
echo.

set PORT=3002
call npm start

pause
