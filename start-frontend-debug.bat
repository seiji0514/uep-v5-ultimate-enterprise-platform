@echo off
setlocal enabledelayedexpansion
chcp 65001
REM UEP v5.0 - フロントエンド起動スクリプト（デバッグ版）
REM このスクリプトは詳細なデバッグ情報を表示します

echo ==========================================
echo UEP v5.0 - フロントエンド起動（デバッグモード）
echo ==========================================
echo.

REM 環境情報を表示
echo [デバッグ情報]
echo スクリプトのパス: %~dp0
echo スクリプトの名前: %~nx0
echo 現在のディレクトリ: %CD%
echo ユーザー: %USERNAME%
echo コンピューター: %COMPUTERNAME%
echo.

REM プロジェクトディレクトリに移動
echo [ステップ1] プロジェクトディレクトリに移動...
cd /d "%~dp0"
if errorlevel 1 (
    echo [エラー] プロジェクトディレクトリに移動できませんでした
    echo 現在のディレクトリ: %CD%
    echo スクリプトのパス: %~dp0
    echo.
    pause
    exit /b 1
)
echo 移動後のディレクトリ: %CD%
echo.

REM フロントエンドディレクトリの確認
echo [ステップ2] フロントエンドディレクトリを確認...
if not exist "frontend" (
    echo [エラー] フロントエンドディレクトリが見つかりません
    echo 現在のディレクトリ: %CD%
    echo 期待されるパス: %CD%\frontend
    echo.
    dir /b
    echo.
    pause
    exit /b 1
)
echo フロントエンドディレクトリ: OK
echo.

REM フロントエンドディレクトリに移動
echo [ステップ3] フロントエンドディレクトリに移動...
cd /d "%~dp0frontend"
if errorlevel 1 (
    echo [エラー] フロントエンドディレクトリに移動できませんでした
    echo 現在のディレクトリ: %CD%
    echo 期待されるパス: %~dp0frontend
    echo.
    pause
    exit /b 1
)
echo 移動後のディレクトリ: %CD%
echo.

REM Node.jsの確認
echo [ステップ4] Node.jsを確認...
where node >nul 2>&1
if errorlevel 1 (
    echo [エラー] Node.jsが見つかりません
    echo PATH環境変数を確認してください
    echo.
    echo PATH: %PATH%
    echo.
    pause
    exit /b 1
)
echo Node.jsのパス:
where node
node --version
echo.

REM npmの確認
echo [ステップ5] npmを確認...
where npm >nul 2>&1
if errorlevel 1 (
    echo [エラー] npmが見つかりません
    echo PATH環境変数を確認してください
    echo.
    pause
    exit /b 1
)
echo npmのパス:
where npm
npm --version
echo.

REM package.jsonの確認
echo [ステップ6] package.jsonを確認...
if not exist "package.json" (
    echo [エラー] package.jsonが見つかりません
    echo 現在のディレクトリ: %CD%
    echo.
    dir /b
    echo.
    pause
    exit /b 1
)
echo package.json: OK
echo.

REM node_modulesの確認
echo [ステップ7] node_modulesを確認...
if not exist "node_modules" (
    echo node_modulesが見つかりません
    echo 依存パッケージをインストールしますか？ (Y/N)
    set /p install_deps=
    if /i "!install_deps!"=="Y" (
        echo 依存パッケージをインストール中...
        call npm install
        if errorlevel 1 (
            echo [エラー] 依存パッケージのインストールに失敗しました
            pause
            exit /b 1
        )
    ) else (
        echo 依存パッケージのインストールをスキップします
        pause
        exit /b 0
    )
) else (
    echo node_modules: OK
)
echo.

REM フロントエンドの起動
echo ==========================================
echo フロントエンドを起動します...
echo ==========================================
echo URL: http://localhost:3000
echo.
echo 停止するには: Ctrl+C を押してください
echo ==========================================
echo.

call npm start

pause
