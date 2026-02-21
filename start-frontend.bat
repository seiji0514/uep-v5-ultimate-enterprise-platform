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
    echo [エラー] プロジェクトディレクトリに移動できませんでした
    echo 現在のディレクトリ: %CD%
    echo スクリプトのパス: %~dp0
    echo.
    pause
    exit /b 1
)

REM フロントエンドディレクトリの確認
if not exist "frontend" (
    echo [エラー] フロントエンドディレクトリが見つかりません
    echo 現在のディレクトリ: %CD%
    echo 期待されるパス: %CD%\frontend
    echo.
    echo フロントエンドを作成しますか？ (Y/N)
    set /p create_frontend=
    if /i "!create_frontend!" EQU "Y" (
        echo フロントエンドを作成中...
        if not exist "frontend" mkdir frontend
        cd /d "%~dp0frontend"

        REM React + TypeScriptプロジェクトを作成
        echo React + TypeScriptプロジェクトを作成中...
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
    echo [エラー] フロントエンドディレクトリに移動できませんでした
    echo 現在のディレクトリ: %CD%
    echo 期待されるパス: %~dp0frontend
    echo.
    pause
    exit /b 1
)

REM Node.jsの確認
echo [1/4] Node.jsを確認中...
node --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ==========================================
    echo [エラー] Node.jsがインストールされていません
    echo ==========================================
    echo Node.jsをインストールしてください
    echo URL: https://nodejs.org/
    echo.
    echo インストール後、このスクリプトを再実行してください
    echo.
    pause
    exit /b 1
)
node --version
echo Node.js: OK

REM npmの確認
echo [2/4] npmを確認中...
npm --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ==========================================
    echo [エラー] npmがインストールされていません
    echo ==========================================
    echo Node.jsと一緒にnpmがインストールされているか確認してください
    echo.
    pause
    exit /b 1
)
npm --version
echo npm: OK

REM package.jsonの確認
echo [3/4] package.jsonを確認中...
if not exist "package.json" (
    echo.
    echo ==========================================
    echo [エラー] package.jsonが見つかりません
    echo ==========================================
    echo フロントエンドディレクトリが正しく設定されているか確認してください
    echo 現在のディレクトリ: %CD%
    echo.
    pause
    exit /b 1
)
echo package.json: OK

REM 依存パッケージのインストール
echo [4/4] 依存パッケージを確認中...
if not exist "node_modules" (
    echo 依存パッケージをインストール中...
    echo これには数分かかる場合があります...
    echo.
    call npm install
    if errorlevel 1 (
        echo.
        echo ==========================================
        echo [エラー] 依存パッケージのインストールに失敗しました
        echo ==========================================
        echo 以下を確認してください:
        echo 1. インターネット接続
        echo 2. npmのバージョン（npm --version）
        echo 3. package.jsonの内容
        echo.
        pause
        exit /b 1
    )
    echo 依存パッケージのインストールが完了しました
) else (
    echo 依存パッケージは既にインストールされています
)

REM フロントエンドの起動
echo.
echo ==========================================
echo フロントエンドを起動中...
echo ==========================================
echo URL: http://localhost:3000
echo.
echo 停止するには: Ctrl+C を押してください
echo ==========================================
echo.

REM npm startを実行
call npm start
if errorlevel 1 (
    echo.
    echo ==========================================
    echo [エラー] フロントエンドの起動に失敗しました
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
