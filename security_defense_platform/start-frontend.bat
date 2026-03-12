@echo off
chcp 65001 >nul
REM 統合セキュリティ・防衛プラットフォーム - フロントエンド起動（ポート3001）

echo ==========================================
echo 統合セキュリティ・防衛プラットフォーム フロントエンド
echo ポート3001
echo ==========================================
echo.

cd /d "%~dp0frontend"

if not exist "package.json" (
    echo エラー: package.json が見つかりません
    pause
    exit /b 1
)

if not exist "node_modules" (
    echo 依存パッケージをインストール中...
    call npm install
)

echo.
echo URL: http://localhost:3001
echo バックエンド（ポート9001）を先に起動してください
echo 停止: Ctrl+C
echo ==========================================
echo.

call npm start

pause
