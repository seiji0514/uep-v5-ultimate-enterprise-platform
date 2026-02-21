@echo off
chcp 65001 >nul
REM UEP v5.0 - バックエンドをキャッシュ削除して再起動

echo ==========================================
echo UEP v5.0 - クリーン再起動
echo ==========================================
echo.

cd /d "%~dp0"
cd backend

REM Pythonプロセスを終了
echo Pythonプロセスを終了中...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

REM __pycache__ を削除
echo キャッシュを削除中...
if exist __pycache__ rmdir /s /q __pycache__
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d" 2>nul

echo.
echo 再起動します...
call "%~dp0start-backend.bat"
