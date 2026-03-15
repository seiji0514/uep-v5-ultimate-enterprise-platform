@echo off
chcp 65001 >nul
REM Google Drive へのバックアップ
REM パスは環境に合わせて変更してください

echo ==========================================
echo Google Drive へのバックアップ
echo ==========================================
echo.

REM Google Drive = N: (My Drive -> drive.google.com)
set "GDRIVE=N:\マイドライブ"
if not exist "N:\" (
    echo [エラー] N: ドライブ（Google Drive）が見つかりません
    pause
    exit /b 1
)

set DEST=%GDRIVE%\uep-v5-backup
set BACKUP_DATE=%date:~0,4%-%date:~5,2%-%date:~8,2%

cd /d "%~dp0.."
set ROOT=%CD%

echo コピー元: %ROOT%
echo コピー先: %DEST%\%BACKUP_DATE%
echo.
if /i not "%1"=="auto" pause

REM 日付フォルダを作成
if not exist "%DEST%" mkdir "%DEST%"
if not exist "%DEST%\%BACKUP_DATE%" mkdir "%DEST%\%BACKUP_DATE%"

REM UEP 本体
echo [1/2] UEP v5.0 をコピー中...
robocopy "%ROOT%" "%DEST%\%BACKUP_DATE%\uep-v5-ultimate-enterprise-platform" /E /XD node_modules venv __pycache__ .git .vscode .idea /XF *.sqlite *.db /NFL /NDL /NJH /NJS /nc /ns /np

REM docs
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
echo Google Drive が同期中であれば、クラウドにアップロードされます
echo.
if /i not "%1"=="auto" pause
