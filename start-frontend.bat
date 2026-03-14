@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
REM UEP v5.0 - フロントエンド起動スクリプト（Windows）

REM ウィンドウがすぐに閉じないように、最初にpauseを追加
REM エラー時にもウィンドウが残るようにする

echo ==========================================
echo UEP v5.0 - フロントエンド起動
echo ==========================================
echo.

REM プロジェクトディレクトリに移動
cd /d "%~dp0"
if errorlevel 1 (
    echo [Error] Cannot change to project directory
    echo 現在のディレクトリ: %CD%
    echo スクリプトのパス: %~dp0
    echo.
    pause
    exit /b 1
)

REM フロントエンドディレクトリの確認
if not exist "frontend" (
    echo [Error] frontend directory not found
    echo 現在のディレクトリ: %CD%
    echo 期待されるパス: %CD%\frontend
    echo.
    echo Create frontend? (Y/N)
    set /p create_frontend=
    if /i "!create_frontend!"=="Y" (
        echo Creating frontend...
        if not exist "frontend" mkdir frontend
        cd /d "%~dp0frontend"

        REM React + TypeScriptプロジェクトを作成
        echo Creating React project...
        call npx create-react-app . --template typescript --yes

        if errorlevel 1 (
            echo [エラー] Reactプロジェクトの作成に失敗しました
            echo Node.jsとnpmがインストールされているか確認してください
            echo.
            pause
            exit /b 1
        )

        echo フロントエンドプロジェクトが作成されました
        cd /d "%~dp0"
    ) else (
        echo フロントエンドの起動をスキップします
        echo.
        pause
        exit /b 0
    )
)

REM フロントエンドディレクトリに移動
cd /d "%~dp0frontend"
if errorlevel 1 (
    echo [Error] Cannot change to frontend directory
    echo 現在のディレクトリ: %CD%
    echo 期待されるパス: %~dp0frontend
    echo.
    pause
    exit /b 1
)

REM Node.jsの確認
echo [1/4] Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ==========================================
    echo [Error] Node.js not installed
    echo ==========================================
    echo Node.jsをインストールしてください
    echo ダウンロード: https^://nodejs.org/
    echo.
    echo インストール後、このスクリプトを再実行してください
    echo.
    pause
    exit /b 1
)
node --version
echo Node.js: OK

REM npmの確認
echo [2/4] Checking npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ==========================================
    echo [Error] npm not installed
    echo ==========================================
    echo Node.jsと一緒にnpmがインストールされているか確認してください
    echo.
    pause
    exit /b 1
)
npm --version
echo npm: OK

REM package.jsonの確認
echo [3/4] Checking package.json...
if not exist "package.json" (
    echo.
    echo ==========================================
    echo [Error] package.json not found
    echo ==========================================
    echo フロントエンドディレクトリが正しく設定されているか確認してください
    echo 現在のディレクトリ: %CD%
    echo.
    pause
    exit /b 1
)
echo package.json: OK

REM 依存パッケージのインストール
echo [4/4] Checking dependencies...
if not exist "node_modules" (
    echo Installing dependencies...
    echo This may take a few minutes...
    echo.
    call npm install
    if errorlevel 1 (
        echo.
        echo ==========================================
        echo [Error] Failed to install dependencies
        echo ==========================================
        echo 以下を確認してください:
        echo 1. インターネット接続
        echo 2. npmのバージョン（npm --version）
        echo 3. package.jsonの内容
        echo.
        pause
        exit /b 1
    )
    echo Dependencies installed.
) else (
    echo Dependencies already installed.
)

REM .envが無ければ.exampleから作成（REACT_APP_EOH_URL等を含む）
if not exist ".env" (
    if exist ".env.example" (
        echo Creating .env from .env.example...
        copy ".env.example" ".env"
    )
)

REM UEP→EOHリンク用（.envに無い場合のフォールバック）
if not defined REACT_APP_EOH_URL set REACT_APP_EOH_URL=http://localhost:3020

REM フロントエンドの起動
echo.
echo ==========================================
echo Starting frontend...
echo ==========================================
echo Open http://localhost:3000 in browser
echo.
echo Stop: Ctrl+C
echo ==========================================
echo.

REM npm startを実行
call npm start
if errorlevel 1 (
    echo.
    echo ==========================================
    echo [Error] Failed to start frontend
    echo ==========================================
    echo 以下を確認してください:
    echo 1. ポート3000が使用されていないか
    echo 2. 依存パッケージが正しくインストールされているか
    echo 3. package.jsonの内容
    echo.
    echo 手動で起動する場合:
    echo   cd frontend
    echo   npm start
    echo.
    pause
    exit /b 1
)

REM 正常終了時もpause（通常はnpm startが終了しない）
pause
