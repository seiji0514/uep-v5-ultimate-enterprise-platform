@echo off
chcp 65001 >nul
REM ポート8000を使用しているプロセスを強制終了（管理者権限推奨）

echo ==========================================
echo ポート8000の解放
echo ==========================================
echo.

cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\kill-and-check-port-8000.ps1"

echo.
echo 完了。start-backend.bat を実行してください。
pause
