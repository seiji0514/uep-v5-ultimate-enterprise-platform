@echo off
chcp 65001 >nul
REM 外付けUSB 2（O:）への定期バックアップ
REM UEP v5.0 + 個人会計 + docs 一式をコピー

echo ==========================================
echo 外付けUSB 2（O:）へのバックアップ
echo ==========================================
echo.

set DEST=O:\uep-v5-backup
set BACKUP_DATE=%date:~0,4%-%date:~5,2%-%date:~8,2%

REM O: ドライブの確認
if not exist "O:\" (
    echo [エラー] O: ドライブが見つかりません
    echo 外付けUSB 2 を接続してください
    pause
    exit /b 1
)

cd /d "%~dp0.."
set ROOT=%CD%

echo コピー元: %ROOT%
echo コピー先: %DEST%\%BACKUP_DATE%
echo.
echo 実行日時: %date% %time%
echo.
if /i not "%1"=="auto" pause

REM 日付フォルダを作成
if not exist "%DEST%" mkdir "%DEST%"
if not exist "%DEST%\%BACKUP_DATE%" mkdir "%DEST%\%BACKUP_DATE%"

REM UEP 本体（除外コピー）
echo [1/2] UEP v5.0 をコピー中...
robocopy "%ROOT%" "%DEST%\%BACKUP_DATE%\uep-v5-ultimate-enterprise-platform" /E /XD node_modules venv venv_wsl __pycache__ .git .vscode .idea /XF *.sqlite *.db /NFL /NDL /NJH /NJS /nc /ns /np

REM docs（職務経歴書・ポートフォリオ等）
if exist "%ROOT%\docs" (
    echo [2/2] docs をコピー中...
    robocopy "%ROOT%\docs" "%DEST%\%BACKUP_DATE%\docs" /E /NFL /NDL /NJH /NJS /nc /ns /np
) else (
    echo [2/2] docs フォルダなし（スキップ）
)

call "%~dp0backup_create_manifest.bat" "%DEST%" "%BACKUP_DATE%"

echo.
echo ==========================================
echo バックアップ完了: %DEST%\%BACKUP_DATE%
echo ==========================================
echo.
echo 次のステップ:
echo   * Google Drive に重要ファイルを同期
echo.
if /i not "%1"=="auto" pause
