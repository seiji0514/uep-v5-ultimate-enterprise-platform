@echo off
chcp 65001 >nul
REM UEP v5.0 - 全サービス停止スクリプト（Windows）

echo ==========================================
echo UEP v5.0 - 全サービス停止
echo ==========================================
echo.

REM バックエンド（ポート8000）を停止
echo バックエンドを停止中...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo プロセス %%a を終了中...
    taskkill /F /PID %%a >nul 2>&1
)

REM フロントエンド（ポート3000）を停止
echo フロントエンドを停止中...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000 ^| findstr LISTENING') do (
    echo プロセス %%a を終了中...
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo 全サービスを停止しました
echo.

pause
