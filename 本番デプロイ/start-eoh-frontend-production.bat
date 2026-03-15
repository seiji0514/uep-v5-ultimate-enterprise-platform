@echo off
chcp 65001 >nul
REM 企業横断オペレーション基盤（EOH）- 本番用 フロントエンド（ビルド＋起動）

echo ==========================================
echo 企業横断オペレーション基盤（EOH）- 本番用 フロントエンド
echo ==========================================
echo.

cd /d "%~dp0"
cd ..

if not exist "enterprise_operations_hub\frontend" (
    echo [Error] enterprise_operations_hub\frontend がありません
    pause
    exit /b 1
)

cd enterprise_operations_hub\frontend

REM .env.production の確認（なければローカル用で作成）
if not exist ".env.production" (
    echo REACT_APP_EOH_API_URL=http://localhost:9020> .env.production
    echo [注意] .env.production をローカル用で作成しました
    echo 本番デプロイ時は REACT_APP_EOH_API_URL を本番APIのURLに変更してください
    echo.
)

set NODE_OPTIONS=--max-old-space-size=8192
set GENERATE_SOURCEMAP=false

echo [1/2] ビルド中...
call npm run build
if errorlevel 1 (
    echo [Error] ビルドに失敗しました
    pause
    exit /b 1
)

if not exist "build" (
    echo [Error] build フォルダがありません
    pause
    exit /b 1
)

echo.
echo [2/2] 起動中: http://localhost:3020
echo 停止: Ctrl+C
echo ==========================================
echo.

npx serve -s build -l 3020
if errorlevel 1 (
    echo [Error] serve が終了しました。ポート3020の使用状況を確認してください
    echo.
)

pause
