@echo off
chcp 65001 >nul
REM USB N と O の既存 uep-v5-backup フォルダへ追加・更新
REM 3/7 等で作成済みの uep-v5-backup に、変更分を上書き・新規を追加
REM
REM 日付フォルダを使う場合: set "USE_DATE=2026-03-07" 等に設定
REM 空の場合は uep-v5-backup\ 直下にコピー（常に最新を更新）

set "USB1=N:"
set "USB2=O:"
set "USE_DATE="
REM 3/7 の日付フォルダを更新する場合: set "USE_DATE=2026-03-07"

echo ==========================================
echo USB N と O へ追加・更新（uep-v5-backup を更新）
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
    echo コピー先: 各 USB の uep-v5-backup\（直下を更新）
) else (
    set "SUBPATH=%USE_DATE%\"
    echo コピー先: 各 USB の uep-v5-backup\%USE_DATE%\（日付フォルダを更新）
)
echo コピー元: %ROOT%
echo 実行日時: %date% %time%
echo.
if /i not "%1"=="auto" pause

REM === USB N ===
echo.
echo ==========================================
echo [1/2] USB N (%USB1%) の uep-v5-backup へ追加・更新
echo ==========================================
if exist "%USB1%\" (
    set "DEST=%USB1%\uep-v5-backup\%SUBPATH%"
    if not exist "%DEST%" mkdir "%DEST%"
    echo コピー先: %USB1%\uep-v5-backup\%SUBPATH%
    robocopy "%ROOT%" "%DEST%uep-v5-ultimate-enterprise-platform" /E /XD node_modules venv __pycache__ .git .vscode .idea /XF *.sqlite *.db /NFL /NDL /NJH /NJS /nc /ns /np
    if exist "%ROOT%\standalone-personal-accounting" robocopy "%ROOT%\standalone-personal-accounting" "%DEST%standalone-personal-accounting" /E /XD venv __pycache__ .git /XF *.sqlite *.db /NFL /NDL /NJH /NJS /nc /ns /np
    if exist "%ROOT%\docs" robocopy "%ROOT%\docs" "%DEST%docs" /E /NFL /NDL /NJH /NJS /nc /ns /np
    call "%~dp0backup_create_manifest.bat" "%USB1%\uep-v5-backup" "%USE_DATE%"
    echo [完了] USB N
) else (
    echo [スキップ] %USB1% が見つかりません
)

REM === USB O ===
echo.
echo ==========================================
echo [2/2] USB O (%USB2%) の uep-v5-backup へ追加・更新
echo ==========================================
if exist "%USB2%\" (
    set "DEST=%USB2%\uep-v5-backup\%SUBPATH%"
    if not exist "%DEST%" mkdir "%DEST%"
    echo コピー先: %USB2%\uep-v5-backup\%SUBPATH%
    robocopy "%ROOT%" "%DEST%uep-v5-ultimate-enterprise-platform" /E /XD node_modules venv __pycache__ .git .vscode .idea /XF *.sqlite *.db /NFL /NDL /NJH /NJS /nc /ns /np
    if exist "%ROOT%\standalone-personal-accounting" robocopy "%ROOT%\standalone-personal-accounting" "%DEST%standalone-personal-accounting" /E /XD venv __pycache__ .git /XF *.sqlite *.db /NFL /NDL /NJH /NJS /nc /ns /np
    if exist "%ROOT%\docs" robocopy "%ROOT%\docs" "%DEST%docs" /E /NFL /NDL /NJH /NJS /nc /ns /np
    call "%~dp0backup_create_manifest.bat" "%USB2%\uep-v5-backup" "%USE_DATE%"
    echo [完了] USB O
) else (
    echo [スキップ] %USB2% が見つかりません
)

echo.
echo ==========================================
echo 追加・更新完了
echo ==========================================
echo.
if /i not "%1"=="auto" pause
