@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
REM UEP v5.0 - USBドライブへのコピー（node_modules, venv を除外）
REM パス長制限・コピーエラーを回避

echo ==========================================
echo UEP v5.0 - USBドライブへのコピー
echo ==========================================
echo.

REM コピー先（N: ドライブ）- 別ドライブの場合はここを編集
set DEST=N:\uep-v5-ultimate-enterprise-platform

REM プロジェクトルートを取得
cd /d "%~dp0.."
set SOURCE=%CD%

REM コピー先の確認
if not exist "N:\" (
    echo [エラー] N: ドライブが見つかりません
    echo USBが接続されているか確認してください
    echo.
    echo 別のドライブにコピーする場合は、このスクリプトの DEST を編集してください
    pause
    exit /b 1
)

echo コピー元: %SOURCE%
echo コピー先: %DEST%
echo.
echo 除外: node_modules, venv, __pycache__, .git, *.sqlite 等
echo （コピー先で pip install と npm install を実行してください）
echo.
pause

REM 既存のコピー先を削除（ある場合）
if exist "%DEST%" (
    echo 既存のフォルダを削除中...
    rmdir /s /q "%DEST%" 2>nul
    if exist "%DEST%" (
        echo [警告] 削除できません。手動で削除してから再実行してください
        pause
        exit /b 1
    )
)

REM robocopy で除外指定してコピー
echo コピー中...（数分かかる場合があります）
robocopy "%SOURCE%" "%DEST%" /E /XD node_modules venv __pycache__ .git .vscode .idea /XF *.sqlite *.db /NFL /NDL /NJH /NJS /nc /ns /np

if errorlevel 8 (
    echo.
    echo [エラー] コピー中にエラーが発生しました
    pause
    exit /b 1
)

echo.
echo ==========================================
echo データコピー完了の確認
echo ==========================================

set VERIFY_OK=1

REM 必須ファイル・フォルダの存在確認
if not exist "%DEST%\backend\main.py" (
    echo [NG] backend\main.py が存在しません
    set VERIFY_OK=0
) else (
    echo [OK] backend\main.py
)

if not exist "%DEST%\backend\requirements.txt" (
    echo [NG] backend\requirements.txt が存在しません
    set VERIFY_OK=0
) else (
    echo [OK] backend\requirements.txt
)

if not exist "%DEST%\frontend\package.json" (
    echo [NG] frontend\package.json が存在しません
    set VERIFY_OK=0
) else (
    echo [OK] frontend\package.json
)

if not exist "%DEST%\start-local.bat" (
    echo [NG] start-local.bat が存在しません
    set VERIFY_OK=0
) else (
    echo [OK] start-local.bat
)

if not exist "%DEST%\README.md" (
    echo [NG] README.md が存在しません
    set VERIFY_OK=0
) else (
    echo [OK] README.md
)

if exist "%DEST%\backend\infra_builder\routes.py" (
    echo [OK] backend\infra_builder\routes.py
)

echo.

if "!VERIFY_OK!"=="0" (
    echo [警告] 一部のファイルがコピーされていません。コピーを再実行してください。
    pause
    exit /b 1
)

echo ==========================================
echo 確認完了: データコピーは正常に完了しました
echo ==========================================
echo.
echo 次のステップ:
echo 1. USBの %DEST% に移動
echo 2. start-local.bat を実行（venv と node_modules が自動作成されます）
echo.
pause
