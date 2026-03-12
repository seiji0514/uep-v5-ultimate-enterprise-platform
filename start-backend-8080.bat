@echo off
chcp 65001 >nul
REM UEP v5.0 - バックエンドAPI起動（ポート8080・8000がWindows予約等で使えない場合）

echo ==========================================
echo UEP v5.0 - バックエンドAPI起動（ポート8080）
echo ==========================================
echo.
echo ※ ポート8000が使用不可のため、8080で起動します
echo    URL: http://localhost:8080
echo    API Docs: http://localhost:8080/docs
echo    フロントエンドの .env で REACT_APP_API_URL=http://localhost:8080 に変更してください
echo.

cd /d "%~dp0"
cd backend

call venv\Scripts\activate.bat 2>nul
if errorlevel 1 (
    echo 仮想環境が見つかりません。先に start-backend.bat を1回実行してください。
    pause
    exit /b 1
)

set PORT=8080
python main.py

pause
