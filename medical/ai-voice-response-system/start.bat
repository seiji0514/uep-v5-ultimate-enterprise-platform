@echo off
chcp 65001 >nul
echo ========================================
echo AI自動音声応答システム 起動スクリプト
echo ========================================
echo.

cd /d "%~dp0"

REM Pythonコマンドを検出（py または python）
set PYTHON_CMD=
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    echo Python Launcher (py) を使用します
) else (
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_CMD=python
        echo python コマンドを使用します
    ) else (
        echo エラー: Pythonがインストールされていません
        echo Python 3.8以上をインストールしてください
        echo または py コマンドが利用可能か確認してください
        pause
        exit /b 1
    )
)

echo.
echo [1/4] Pythonのバージョン確認...
%PYTHON_CMD% --version
if errorlevel 1 (
    echo エラー: Pythonのバージョン確認に失敗しました
    pause
    exit /b 1
)

echo.
echo [2/4] 依存関係の確認...
%PYTHON_CMD% -m pip list | findstr "fastapi" >nul
if errorlevel 1 (
    echo 依存関係をインストール中...
    echo 初回インストールには時間がかかります...
    %PYTHON_CMD% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo エラー: 依存関係のインストールに失敗しました
        echo 手動でインストールしてください: %PYTHON_CMD% -m pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo 依存関係のインストールが完了しました
) else (
    echo 依存関係は既にインストールされています
)

echo.
echo [3/4] 設定ファイルの確認...
if not exist ".env" (
    echo .envファイルが見つかりません
    echo オプション: .envファイルを作成してOpenAI API Keyを設定できます
    echo ローカルモデルのみ使用する場合は設定不要です
)

echo.
echo [4/4] バックエンドサーバーを起動中...
echo.
echo ========================================
echo サーバー起動完了後、ブラウザで以下を開いてください:
echo ポート番号は設定ファイル（config.py）または環境変数（SERVER_PORT）で変更できます
echo デフォルト: http://localhost:8000
echo ========================================
echo.
echo 停止するには Ctrl+C を押してください
echo.

cd backend
%PYTHON_CMD% main.py

if errorlevel 1 (
    echo.
    echo エラーが発生しました
    echo ログを確認してください
    pause
)
