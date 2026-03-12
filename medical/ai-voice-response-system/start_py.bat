@echo off
chcp 65001 >nul
echo ========================================
echo AI自動音声応答システム 起動スクリプト
echo Python Launcher (py) を使用
echo ========================================
echo.

cd /d "%~dp0"

REM pyコマンドでstart.pyを実行
py start.py

if errorlevel 1 (
    echo.
    echo エラーが発生しました
    echo py コマンドが利用できない場合は、start.bat を試してください
    pause
)
