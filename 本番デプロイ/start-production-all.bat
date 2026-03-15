@echo off
chcp 65001 >nul
REM UEP v5.0 - 本番デプロイ用 一括起動（バックエンド＋フロントエンド）

echo ==========================================
echo UEP v5.0 - 本番モード 一括起動
echo ==========================================
echo.
echo 1. バックエンドを別ウィンドウで起動します
echo 2. フロントエンドをビルドして起動します
echo.

cd /d "%~dp0.."
set "ROOT=%CD%"

REM バックエンドを別ウィンドウで起動（ランチャー経由で日本語パスを回避）
start "UEP Backend (Production)" cmd /k "%ROOT%\start-backend-production-launcher.bat"

REM バックエンドの起動待ち
echo バックエンドの起動を待機中...
timeout /t 5 /nobreak >nul

REM フロントエンドを別ウィンドウで起動（ビルド＋serve）
start "UEP Frontend (Production)" cmd /k "%ROOT%\start-frontend-production-launcher.bat"

echo.
echo バックエンド・フロントエンドを別ウィンドウで起動しました
echo 終了するには各ウィンドウで Ctrl+C を押してください
echo.
pause
