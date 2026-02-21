@echo off
chcp 65001 >nul
REM UEP v5.0 - バックエンドとフロントエンドを同時起動（Windows）

echo ==========================================
echo UEP v5.0 - 全サービス起動
echo ==========================================
echo.

REM プロジェクトディレクトリに移動
cd /d "%~dp0"

REM バックエンドとフロントエンドを別ウィンドウで起動
echo バックエンドとフロントエンドを起動中...
echo.
echo 注意: バックエンドの起動には数秒かかる場合があります
echo.

REM バックエンドを新しいウィンドウで起動
start "UEP v5.0 - Backend API" cmd /k "%~dp0start-backend.bat"

REM 少し待機（バックエンドの起動を待つ）
timeout /t 3 /nobreak >nul

REM フロントエンドを新しいウィンドウで起動
start "UEP v5.0 - Frontend" cmd /k "%~dp0start-frontend.bat"

echo.
echo ==========================================
echo 起動完了
echo.
echo バックエンド: http://localhost:8000
echo フロントエンド: http://localhost:3000
echo.
echo 各ウィンドウを閉じることで停止できます
echo ==========================================
echo.

pause
