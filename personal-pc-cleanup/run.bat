@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
cd /d "%~dp0"

echo ==========================================
echo 個人用 PC 容量確保ツール
echo ==========================================
echo.

REM Python 確認
python --version >nul 2>&1
if errorlevel 1 (
    echo [エラー] Python がインストールされていません
    echo https://www.python.org/ からインストールしてください
    pause
    exit /b 1
)

echo 1. 検出のみ（削除しない）
echo 2. Docker クリーンアップ実行
echo 3. Cドライブ + 一時フォルダ スキャン＆削除
echo 4. 全て実行（検出 + Docker + Cドライブ削除）
echo.
set /p choice="番号を入力 (1-4, 省略=1): "
if "%choice%"=="" set choice=1

if "%choice%"=="1" (
    python cleanup.py --detect --all
) else if "%choice%"=="2" (
    python cleanup.py --detect --docker
    echo.
    set /p do_clean="Docker クリーンアップを実行しますか？ (y/N): "
    if /i "!do_clean!"=="y" python cleanup.py --clean --docker
) else if "%choice%"=="3" (
    python cleanup.py --detect --c-drive --temp
    echo.
    set /p do_clean="削除を実行しますか？ (y/N): "
    if /i "!do_clean!"=="y" python cleanup.py --clean --c-drive --temp
) else if "%choice%"=="4" (
    python cleanup.py --detect --all --docker
    echo.
    set /p do_clean="Docker + Cドライブの削除を実行しますか？ (y/N): "
    if /i "!do_clean!"=="y" (
        python cleanup.py --clean --docker
        python cleanup.py --clean --c-drive --temp
    )
) else (
    python cleanup.py --detect --all
)

echo.
pause
