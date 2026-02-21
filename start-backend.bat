@echo off
chcp 65001 >nul
REM UEP v5.0 - バックエンドAPI起動スクリプト（Windows）

echo ==========================================
echo UEP v5.0 - バックエンドAPI起動
echo ==========================================
echo.

REM プロジェクトディレクトリに移動
cd /d "%~dp0"

REM Pythonの確認
python --version >nul 2>&1
if errorlevel 1 (
    echo エラー: Pythonがインストールされていません
    echo Python 3.11以上をインストールしてください
    pause
    exit /b 1
)

REM バックエンドディレクトリに移動
cd backend

REM ポート8000を使用しているプロセスを解放
echo ポート8000の解放を確認中...
set USE_PORT=8000
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\kill-and-check-port-8000.ps1"
if errorlevel 1 (
    echo.
    echo ポート8000が使用中のため、ポート8001で起動します。
    echo URL: http://localhost:8001
    echo 診断時: set PORT=8001 ^&^& python test_chaos_endpoint.py
    echo.
    set USE_PORT=8001
)

REM 仮想環境の作成
if not exist "venv" (
    echo 仮想環境を作成中...
    python -m venv venv
    if errorlevel 1 (
        echo エラー: 仮想環境の作成に失敗しました
        echo 管理者権限で実行するか、venvフォルダを手動で削除してください
        pause
        exit /b 1
    )
)

REM 仮想環境の有効化
echo 仮想環境を有効化中...
if not exist "venv\Scripts\activate.bat" (
    echo エラー: 仮想環境が破損しています。再作成します...
    rmdir /s /q venv >nul 2>&1
    python -m venv venv
    if errorlevel 1 (
        echo エラー: 仮想環境の再作成に失敗しました
        pause
        exit /b 1
    )
)
call venv\Scripts\activate.bat

REM 依存パッケージのインストール
echo 依存パッケージをインストール中...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM 環境変数の設定（.envファイルがない場合）
if not exist ".env" (
    echo .envファイルを作成中...
    (
        echo DATABASE_URL=sqlite:///./uep_db.sqlite
        echo REDIS_URL=redis://localhost:6379/0
        echo SECRET_KEY=your-secret-key-change-in-production
    ) > .env
)

REM 起動直前にもポートを再確認（USE_PORT=8000の場合のみ）
if "%USE_PORT%"=="8000" (
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }; Start-Sleep -Seconds 2" >nul 2>&1
)

REM バックエンドAPIの起動
echo.
echo ==========================================
echo バックエンドAPIを起動中...
set PORT=%USE_PORT%
echo URL: http://localhost:%USE_PORT%
echo API Docs: http://localhost:%USE_PORT%/docs
echo.
echo 停止: Ctrl+C
echo ==========================================
echo.

python main.py

pause
