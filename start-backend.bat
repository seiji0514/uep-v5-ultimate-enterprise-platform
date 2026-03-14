@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
REM UEP v5.0 - バックエンドAPI起動スクリプト（Windows）※常に本番モード

echo ==========================================
echo UEP v5.0 - バックエンドAPI起動
echo ==========================================
echo.

REM プロジェクトディレクトリに移動
cd /d "%~dp0"

REM Pythonの確認
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not installed. Install Python 3.11+
    pause
    exit /b 1
)

REM バックエンドディレクトリに移動
cd backend

REM ポート8080を使用（8000はWindows予約範囲7938-8037に含まれる場合あり）
set USE_PORT=8080
echo Port: %USE_PORT%

REM 仮想環境の作成
if not exist "venv" (
    echo Creating venv...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create venv
        echo Run as admin or delete venv folder manually
        pause
        exit /b 1
    )
)

REM 仮想環境の有効化
echo Activating venv...
if not exist "venv\Scripts\activate.bat" (
    echo Error: venv corrupted. Recreating...
    rmdir /s /q venv >nul 2>&1
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to recreate venv
        pause
        exit /b 1
    )
)
call venv\Scripts\activate.bat

REM 依存パッケージのインストール
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM 環境変数の設定（.envファイルがない場合）
if not exist ".env" (
    echo .envファイルを作成中（本番用）...
    for /f "delims=" %%i in ('powershell -NoProfile -Command "[BitConverter]::ToString([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32)).Replace('-','').ToLower()"') do set GEN_KEY=%%i
    (
        echo ENVIRONMENT=production
        echo DEBUG=false
        echo DATABASE_URL=sqlite:///./uep_db.sqlite
        echo REDIS_URL=redis://localhost:6379/0
        echo SECRET_KEY=!GEN_KEY!
        echo PRODUCTION_USERS_FILE=./data/production_users.json
    ) > .env
)

REM 既存 .env に PRODUCTION_USERS_FILE が無い場合は追記
if exist ".env" (
    findstr /C:"PRODUCTION_USERS_FILE" .env >nul 2>&1
    if errorlevel 1 (
        echo PRODUCTION_USERS_FILE=./data/production_users.json>>.env
        echo Added PRODUCTION_USERS_FILE to .env
    )
)

REM 既存 .env で SECRET_KEY が空の場合は生成して更新
powershell -NoProfile -ExecutionPolicy Bypass -Command "$f='.env';if(Test-Path $f){$c=Get-Content $f -Raw;$k=[BitConverter]::ToString([Security.Cryptography.RandomNumberGenerator]::GetBytes(32)).Replace('-','').ToLower();if($c -match 'SECRET_KEY=\s*$' -or $c -match 'SECRET_KEY=change-this'){(Get-Content $f)-replace 'SECRET_KEY=.*',('SECRET_KEY='+$k)|Set-Content $f}}" 2>nul

REM data ディレクトリを用意
if not exist "data" mkdir data

REM 本番モードで起動（常に）
set ENVIRONMENT=production
set DEBUG=false

REM 起動直前にもポートを再確認（USE_PORT=8000の場合のみ）
if "%USE_PORT%"=="8000" (
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }; Start-Sleep -Seconds 2" >nul 2>&1
)

REM バックエンドAPIの起動
echo.
echo ==========================================
echo Starting backend API...
set PORT=%USE_PORT%
echo URL: http://localhost:%USE_PORT%
echo API Docs: disabled in production
echo.
echo Stop: Ctrl+C
echo ==========================================
echo.

python main.py

pause
