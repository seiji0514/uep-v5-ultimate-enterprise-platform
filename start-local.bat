@echo off
chcp 65001 >nul
REM UEP v5.0 - ローカルのみで起動（バックエンド + フロントエンド）
REM ※ クラウド（Vercel/Render）は使用しません

echo ==========================================
echo UEP v5.0 - ローカル起動
echo ==========================================
echo.
echo バックエンド: http://localhost:8000
echo フロントエンド: http://localhost:3000
echo.
echo フロントエンドの .env で REACT_APP_API_URL=http://localhost:8000 を確認してください
echo （ポート8000が使用中の場合はバックエンドが8001で起動します。その場合は .env を 8001 に変更）
echo ==========================================
echo.

call "%~dp0start-all.bat"
