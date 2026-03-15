@echo off
chcp 65001 >nul
REM USB O + 外付けドライブ N + Google Drive P マイドライブ への一括バックアップ

echo ==========================================
echo バックアップ: USB O / 外付け N / Google Drive P
echo ==========================================
echo.

cd /d "%~dp0.."
set ROOT=%CD%
set BACKUP_DATE=%date:~0,4%-%date:~5,2%-%date:~8,2%
echo コピー元: %ROOT%
echo 日付: %BACKUP_DATE%
echo 実行日時: %date% %time%
echo.
if /i not "%1"=="auto" pause

REM === 1. USB O ===
echo.
echo [1/3] USB O (O:\uep-v5-backup) へバックアップ
if exist "O:\" (
    set "DEST=O:\uep-v5-backup"
    if not exist "%DEST%\%BACKUP_DATE%" mkdir "%DEST%\%BACKUP_DATE%"
    robocopy "%ROOT%" "%DEST%\%BACKUP_DATE%\uep-v5-ultimate-enterprise-platform" /E /XD node_modules venv venv_wsl __pycache__ .git .vscode .idea /XF *.sqlite *.db /NFL /NDL /NJH /NJS /nc /ns /np
    if exist "%ROOT%\docs" robocopy "%ROOT%\docs" "%DEST%\%BACKUP_DATE%\docs" /E /NFL /NDL /NJH /NJS /nc /ns /np
    call "%~dp0backup_create_manifest.bat" "%DEST%" "%BACKUP_DATE%"
    echo [完了] USB O
) else (
    echo [スキップ] O: が見つかりません
)

REM === 2. 外付けドライブ N ===
echo.
echo [2/3] 外付けドライブ N (N:\uep-v5-backup) へバックアップ
if exist "N:\" (
    set "DEST=N:\uep-v5-backup"
    if not exist "%DEST%\%BACKUP_DATE%" mkdir "%DEST%\%BACKUP_DATE%"
    robocopy "%ROOT%" "%DEST%\%BACKUP_DATE%\uep-v5-ultimate-enterprise-platform" /E /XD node_modules venv venv_wsl __pycache__ .git .vscode .idea /XF *.sqlite *.db /NFL /NDL /NJH /NJS /nc /ns /np
    if exist "%ROOT%\docs" robocopy "%ROOT%\docs" "%DEST%\%BACKUP_DATE%\docs" /E /NFL /NDL /NJH /NJS /nc /ns /np
    call "%~dp0backup_create_manifest.bat" "%DEST%" "%BACKUP_DATE%"
    echo [完了] 外付けドライブ N
) else (
    echo [スキップ] N: が見つかりません
)

REM === 3. Google Drive P マイドライブ ===
echo.
echo [3/3] Google Drive P マイドライブ (P:\マイドライブ\uep-v5-backup) へバックアップ
if exist "P:\マイドライブ\" (
    set "DEST=P:\マイドライブ\uep-v5-backup"
    if not exist "%DEST%\%BACKUP_DATE%" mkdir "%DEST%\%BACKUP_DATE%"
    robocopy "%ROOT%" "%DEST%\%BACKUP_DATE%\uep-v5-ultimate-enterprise-platform" /E /XD node_modules venv venv_wsl __pycache__ .git .vscode .idea /XF *.sqlite *.db /NFL /NDL /NJH /NJS /nc /ns /np
    if exist "%ROOT%\docs" robocopy "%ROOT%\docs" "%DEST%\%BACKUP_DATE%\docs" /E /NFL /NDL /NJH /NJS /nc /ns /np
    call "%~dp0backup_create_manifest.bat" "%DEST%" "%BACKUP_DATE%"
    echo [完了] Google Drive P
) else (
    echo [スキップ] P:\マイドライブ が見つかりません
)

echo.
echo ==========================================
echo バックアップ完了
echo ==========================================
if /i not "%1"=="auto" pause
