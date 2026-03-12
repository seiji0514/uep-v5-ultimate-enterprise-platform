@echo off
chcp 65001 >nul
echo ========================================
echo 完全統合AI音声応答プラットフォーム
echo ========================================
echo.

REM Pythonコマンドを検出
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=py
    echo Pythonコマンド: py
) else (
    where python >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set PYTHON_CMD=python
        echo Pythonコマンド: python
    ) else (
        echo エラー: Pythonがインストールされていません
        pause
        exit /b 1
    )
)

echo.
echo サーバーを起動しています...
echo.

cd backend
%PYTHON_CMD% main.py

pause
