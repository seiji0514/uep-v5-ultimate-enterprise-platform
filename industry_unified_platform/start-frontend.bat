@echo off
chcp 65001 >nul
REM 産業統合プラットフォーム フロントエンド起動（ポート3010）

echo ==========================================
echo 産業統合プラットフォーム フロントエンド
echo 製造・IoT + 医療・ヘルスケア + 金融・FinTech
echo ポート3010
echo ==========================================
echo.

cd /d "%~dp0frontend"

if not exist "node_modules" (
    echo npm install を実行します...
    call npm install
)

set PORT=3010
set REACT_APP_INDUSTRY_API_URL=http://localhost:9010

echo URL: http://localhost:3010
echo バックエンド: http://localhost:9010
echo ==========================================
echo.

call npm start

pause
