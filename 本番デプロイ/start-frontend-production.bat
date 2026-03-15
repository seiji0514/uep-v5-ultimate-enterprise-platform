@echo off
chcp 65001 >nul
REM UEP v5.0 - 本番デプロイ用 フロントエンド（ビルド＋起動）

echo ==========================================
echo UEP v5.0 - 本番用 フロントエンド
echo ==========================================
echo.

cd /d "%~dp0"
cd ..

if not exist "frontend" (
    echo [Error] frontend ディレクトリがありません
    pause
    exit /b 1
)

cd frontend

REM .env.production の確認
if not exist ".env.production" (
    echo [注意] .env.production がありません
    echo 本番デプロイ\本番デプロイ手順.md を参照して設定してください
    echo.
    pause
    exit /b 1
)

REM メモリ対策
set NODE_OPTIONS=--max-old-space-size=8192
set GENERATE_SOURCEMAP=false

echo [1/2] ビルド中...
call npm run build
if errorlevel 1 (
    echo.
    echo [Error] ビルドに失敗しました
    pause
    exit /b 1
)

REM build フォルダの確認
if not exist "build" (
    echo [Error] build フォルダがありません。ビルドに失敗している可能性があります
    pause
    exit /b 1
)

echo.
echo [2/2] 起動中: http://localhost:3000
echo.

REM ポート3000の使用確認（LISTENING状態のみ・誤検知を防止）
netstat -ano | findstr "LISTENING" | findstr ":3000" >nul 2>&1
if not errorlevel 1 (
    echo [注意] ポート3000は既に使用中です
    echo 既存のフロントエンドを停止してから再実行してください
    echo.
    echo 確認: netstat -ano ^| findstr :3000
    echo.
    pause
    exit /b 1
)

echo 停止: Ctrl+C
echo ==========================================
echo.

npx serve -s build -l 3000
if errorlevel 1 (
    echo.
    echo [Error] serve が終了しました。ポート3000の使用状況を確認してください
    echo 例: netstat -ano ^| findstr :3000
    echo.
)

pause
