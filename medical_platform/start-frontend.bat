@echo off
chcp 65001 >nul
REM 医療・ヘルスケアプラットフォーム フロントエンド起動（ポート3003）

echo ==========================================
echo 医療・ヘルスケアプラットフォーム フロントエンド
echo ポート3003
echo ==========================================
echo.

cd /d "%~dp0frontend"

if not exist "node_modules" (
    echo npm install を実行します...
    call npm install
)

echo.
echo URL: http://localhost:3003
echo バックエンド: http://localhost:9003
echo ==========================================
echo.

set PORT=3003
call npm start

pause
