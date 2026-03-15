@echo off
chcp 65001 >nul
REM 一括バックアップ: 外付けUSB 2台 + Google Drive + 外付けドライブ
REM UEP v5.0 + 個人会計 + docs 一式を各先へコピー
REM
REM ドライブレターは環境に合わせて scripts\一括バックアップ_設定.txt で変更可能
REM またはこのファイルの上部の set を編集してください

echo ==========================================
echo 一括バックアップ（外付けUSB 2台 + Google Drive + 外付けドライブ）
echo ==========================================
echo.

REM === ドライブ設定（環境に合わせて変更） ===
REM 外付けドライブ N（ELECOM USBHDD 等）
set "USB1=N:"
REM Google Drive O のマイドライブ（O: が Google Drive の場合）
set "USB2=O:"
set "GDRIVE="
REM その他（別の Google Drive パス等）。空の場合は [3/4] をスキップ
REM set "GDRIVE=G:\マイドライブ"
set "EXT_DRIVE=E:"
REM 使わない場合: set "EXT_DRIVE="
echo.

cd /d "%~dp0.."
set ROOT=%CD%
set BACKUP_DATE=%date:~0,4%-%date:~5,2%-%date:~8,2%

REM === バックアップ対象の事前確認 ===
echo [確認] バックアップ対象フォルダ
set "MISSING="
if not exist "%ROOT%\backend" set "MISSING=%MISSING% backend"
if not exist "%ROOT%\frontend" set "MISSING=%MISSING% frontend"
if not exist "%ROOT%\docs" set "MISSING=%MISSING% docs"
if defined MISSING (
    echo   [注意] 以下のフォルダが見つかりません:%MISSING%
) else (
    echo   - uep-v5-ultimate-enterprise-platform ^(backend, frontend, 各プラットフォーム^)
    echo   - docs
)
echo.

echo コピー元: %ROOT%
echo 日付フォルダ: %BACKUP_DATE%
echo 実行日時: %date% %time%
echo.
if /i not "%1"=="auto" pause

REM === 1. 外付けドライブ N ===
echo.
echo ==========================================
echo [1/4] 外付けドライブ N (%USB1%) へバックアップ
echo ==========================================
if exist "%USB1%\" (
    set "DEST=%USB1%\uep-v5-backup"
    if not exist "%DEST%" mkdir "%DEST%"
    if not exist "%DEST%\%BACKUP_DATE%" mkdir "%DEST%\%BACKUP_DATE%"
    echo コピー先: %DEST%\%BACKUP_DATE%
    robocopy "%ROOT%" "%DEST%\%BACKUP_DATE%\uep-v5-ultimate-enterprise-platform" /E /XD node_modules venv venv_wsl __pycache__ .git .vscode .idea /XF *.sqlite *.db /NFL /NDL /NJH /NJS /nc /ns /np
    if exist "%ROOT%\docs" robocopy "%ROOT%\docs" "%DEST%\%BACKUP_DATE%\docs" /E /NFL /NDL /NJH /NJS /nc /ns /np
    call "%~dp0backup_create_manifest.bat" "%DEST%" "%BACKUP_DATE%"
    echo [完了] USB 1
) else (
    echo [スキップ] %USB1% が見つかりません（外付けドライブ N を接続してください）
)

REM === 2. Google Drive O ===
echo.
echo ==========================================
echo [2/4] Google Drive O (%USB2%) へバックアップ
echo ==========================================
if exist "%USB2%\" (
    set "DEST=%USB2%\uep-v5-backup"
    if not exist "%DEST%" mkdir "%DEST%"
    if not exist "%DEST%\%BACKUP_DATE%" mkdir "%DEST%\%BACKUP_DATE%"
    echo コピー先: %DEST%\%BACKUP_DATE%
    robocopy "%ROOT%" "%DEST%\%BACKUP_DATE%\uep-v5-ultimate-enterprise-platform" /E /XD node_modules venv venv_wsl __pycache__ .git .vscode .idea /XF *.sqlite *.db /NFL /NDL /NJH /NJS /nc /ns /np
    if exist "%ROOT%\docs" robocopy "%ROOT%\docs" "%DEST%\%BACKUP_DATE%\docs" /E /NFL /NDL /NJH /NJS /nc /ns /np
    call "%~dp0backup_create_manifest.bat" "%DEST%" "%BACKUP_DATE%"
    echo [完了] USB 2
) else (
    echo [スキップ] %USB2% が見つかりません（Google Drive O を接続してください）
)

REM === 3. Google Drive（GDRIVE パス指定時・USB2 と別の場合） ===
echo.
echo ==========================================
echo [3/4] Google Drive へバックアップ
echo ==========================================
if "%GDRIVE%"=="" (
    echo [スキップ] GDRIVE 未設定（USB2=O: で [2/4] にバックアップ済み）
) else if exist "%GDRIVE%\" (
    set "DEST=%GDRIVE%\uep-v5-backup"
    if not exist "%DEST%" mkdir "%DEST%"
    if not exist "%DEST%\%BACKUP_DATE%" mkdir "%DEST%\%BACKUP_DATE%"
    echo コピー先: %DEST%\%BACKUP_DATE%
    robocopy "%ROOT%" "%DEST%\%BACKUP_DATE%\uep-v5-ultimate-enterprise-platform" /E /XD node_modules venv venv_wsl __pycache__ .git .vscode .idea /XF *.sqlite *.db /NFL /NDL /NJH /NJS /nc /ns /np
    if exist "%ROOT%\docs" robocopy "%ROOT%\docs" "%DEST%\%BACKUP_DATE%\docs" /E /NFL /NDL /NJH /NJS /nc /ns /np
    call "%~dp0backup_create_manifest.bat" "%DEST%" "%BACKUP_DATE%"
    echo [完了] Google Drive
) else (
    echo [スキップ] Google Drive が見つかりません（%GDRIVE%）
)

REM === 4. 外付けドライブ ===
echo.
echo ==========================================
echo [4/4] 外付けドライブ (%EXT_DRIVE%) へバックアップ
echo ==========================================
if "%EXT_DRIVE%"=="" (
    echo [スキップ] 外付けドライブ未設定（設定する場合は set EXT_DRIVE= を編集）
) else if exist "%EXT_DRIVE%\" (
    set "DEST=%EXT_DRIVE%\uep-v5-backup"
    if not exist "%DEST%" mkdir "%DEST%"
    if not exist "%DEST%\%BACKUP_DATE%" mkdir "%DEST%\%BACKUP_DATE%"
    echo コピー先: %DEST%\%BACKUP_DATE%
    robocopy "%ROOT%" "%DEST%\%BACKUP_DATE%\uep-v5-ultimate-enterprise-platform" /E /XD node_modules venv venv_wsl __pycache__ .git .vscode .idea /XF *.sqlite *.db /NFL /NDL /NJH /NJS /nc /ns /np
    if exist "%ROOT%\docs" robocopy "%ROOT%\docs" "%DEST%\%BACKUP_DATE%\docs" /E /NFL /NDL /NJH /NJS /nc /ns /np
    call "%~dp0backup_create_manifest.bat" "%DEST%" "%BACKUP_DATE%"
    echo [完了] 外付けドライブ
) else (
    echo [スキップ] %EXT_DRIVE% が見つかりません（外付けドライブを接続してください）
)

echo.
echo ==========================================
echo 一括バックアップ完了
echo ==========================================
echo.
echo 推奨頻度: 日次〜週次（複数システム構築中は日次推奨）
echo.
if /i not "%1"=="auto" pause
