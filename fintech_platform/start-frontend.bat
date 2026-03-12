@echo off
chcp 65001 >nul
REM 金融・FinTechプラットフォーム フロントエンド起動（ポート3004）

echo ==========================================
echo 金融・FinTechプラットフォーム フロントエンド
echo ポート3004
echo ==========================================
echo.

cd /d "%~dp0frontend"

if not exist "node_modules" (
    echo npm install を実行します...
    call npm install
)

echo.
echo URL: http://localhost:3004
echo バックエンド: http://localhost:9004
echo ==========================================
echo.

set PORT=3004
call npm start

pause
