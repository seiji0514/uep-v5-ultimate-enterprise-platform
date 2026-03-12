@echo off
chcp 65001 >nul
REM 外付けドライブ N と Google Drive の既存 uep-v5-backup フォルダへ追加・更新
REM USB N と O と同じ様に、日付フォルダなしで既存フォルダを更新
REM
REM 日付フォルダを使う場合: set "USE_DATE=2026-03-07" 等に設定
REM 空の場合は uep-v5-backup\ 直下にコピー（常に最新を更新）

REM 外付けドライブ N（ELECOM USBHDD 等）
set "EXT_N=N:"
REM Google Drive O のマイドライブ（O: が Google Drive の場合）
set "GDRIVE=O:\"
set "USE_DATE="
REM 3/7 の日付フォルダを更新する場合: set "USE_DATE=2026-03-07"

echo ==========================================
echo 外付けドライブ N と Google Drive へ追加・更新（uep-v5-backup を更新）
echo ==========================================
echo.

cd /d "%~dp0.."
set ROOT=%CD%

REM === バックアップ対象の事前確認 ===
echo [確認] バックアップ対象
if exist "%ROOT%\backend" (echo   - uep-v5-ultimate-enterprise-platform) else (echo   [注意] backend が見つかりません)
if exist "%ROOT%\docs" (echo   - docs) else (echo   [注意] docs が見つかりません)
echo.

if "%USE_DATE%"=="" (
    set "SUBPATH="
    echo コピー先: 各先の uep-v5-backup\（直下を更新）
) else (
    set "SUBPATH=%USE_DATE%\"
    echo コピー先: 各先の uep-v5-backup\%USE_DATE%\（日付フォルダを更新）
)
echo コピー元: %ROOT%
echo 実行日時: %date% %time%
echo.
if /i not "%1"=="auto" pause

REM === 外付けドライブ N ===
echo.
echo ==========================================
echo [1/2] 外付けドライブ N (%EXT_N%) の uep-v5-backup へ追加・更新
echo ==========================================
if exist "%EXT_N%\" (
    set "DEST=%EXT_N%\uep-v5-backup\%SUBPATH%"
    if not exist "%DEST%" mkdir "%DEST%"
    echo コピー先: %EXT_N%\uep-v5-backup\%SUBPATH%
    robocopy "%ROOT%" "%DEST%uep-v5-ultimate-enterprise-platform" /E /XD node_modules venv __pycache__ .git .vscode .idea /XF *.sqlite *.db /NFL /NDL /NJH /NJS /nc /ns /np
    if exist "%ROOT%\standalone-personal-accounting" robocopy "%ROOT%\standalone-personal-accounting" "%DEST%standalone-personal-accounting" /E /XD venv __pycache__ .git /XF *.sqlite *.db /NFL /NDL /NJH /NJS /nc /ns /np
    if exist "%ROOT%\docs" robocopy "%ROOT%\docs" "%DEST%docs" /E /NFL /NDL /NJH /NJS /nc /ns /np
    call "%~dp0backup_create_manifest.bat" "%EXT_N%\uep-v5-backup" "%USE_DATE%"
    echo [完了] 外付けドライブ N
) else (
    echo [スキップ] %EXT_N% が見つかりません（外付けドライブ N を接続してください）
)

REM === Google Drive ===
echo.
echo ==========================================
echo [2/2] Google Drive の uep-v5-backup へ追加・更新
echo ==========================================
if exist "%GDRIVE%\" (
    set "DEST=%GDRIVE%\uep-v5-backup\%SUBPATH%"
    if not exist "%DEST%" mkdir "%DEST%"
    echo コピー先: %GDRIVE%\uep-v5-backup\%SUBPATH%
    robocopy "%ROOT%" "%DEST%uep-v5-ultimate-enterprise-platform" /E /XD node_modules venv __pycache__ .git .vscode .idea /XF *.sqlite *.db /NFL /NDL /NJH /NJS /nc /ns /np
    if exist "%ROOT%\standalone-personal-accounting" robocopy "%ROOT%\standalone-personal-accounting" "%DEST%standalone-personal-accounting" /E /XD venv __pycache__ .git /XF *.sqlite *.db /NFL /NDL /NJH /NJS /nc /ns /np
    if exist "%ROOT%\docs" robocopy "%ROOT%\docs" "%DEST%docs" /E /NFL /NDL /NJH /NJS /nc /ns /np
    call "%~dp0backup_create_manifest.bat" "%GDRIVE%\uep-v5-backup" "%USE_DATE%"
    echo [完了] Google Drive
) else (
    echo [スキップ] Google Drive が見つかりません
    echo   %GDRIVE% を確認してください。ドライブレターが異なる場合はスクリプト上部の set GDRIVE= を編集
)

echo.
echo ==========================================
echo 追加・更新完了
echo ==========================================
echo.
if /i not "%1"=="auto" pause
