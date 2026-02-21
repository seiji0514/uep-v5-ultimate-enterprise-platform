@echo off
chcp 65001 >nul
echo ==========================================
echo UEP v5.0 - バックエンド再構築スクリプト
echo ==========================================
echo.

cd /d "%~dp0backend"

echo [1/6] Pythonプロセスを終了中...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul
echo Pythonプロセスを終了しました。
echo.

echo [2/6] 仮想環境を削除中...
if exist venv (
    echo 既存の仮想環境を削除しています...
    echo ファイルがロックされている場合は、手動で削除してください。
    echo.
    
    REM まず、Scriptsフォルダを削除
    if exist venv\Scripts (
        echo Scriptsフォルダを削除中...
        rmdir /s /q venv\Scripts >nul 2>&1
    )
    
    REM 次に、Libフォルダを削除
    if exist venv\Lib (
        echo Libフォルダを削除中...
        rmdir /s /q venv\Lib >nul 2>&1
    )
    
    REM 最後に、残りのファイルを削除
    if exist venv (
        echo 残りのファイルを削除中...
        rmdir /s /q venv >nul 2>&1
    )
    
    if exist venv (
        echo.
        echo 警告: 仮想環境の完全な削除に失敗しました。
        echo 以下の手順で手動で削除してください:
        echo   1. すべてのコマンドプロンプトとエディタを閉じる
        echo   2. backend\venv フォルダを手動で削除
        echo   3. このスクリプトを再実行
        echo.
        echo または、rebuild-backend-safe.bat を使用してください。
        echo.
        echo 安全版スクリプトを使用する場合は、Enterキーを押してください。
        pause
        echo.
        echo 安全版スクリプトを実行します...
        cd /d "%~dp0"
        call rebuild-backend-safe.bat
        exit /b 0
    )
    echo 仮想環境を削除しました。
) else (
    echo 仮想環境は存在しません。
)
echo.

echo [3/6] 新しい仮想環境を作成中...
python -m venv venv
if errorlevel 1 (
    echo エラー: 仮想環境の作成に失敗しました。
    echo Pythonがインストールされているか確認してください。
    pause
    exit /b 1
)
echo 仮想環境を作成しました。
echo.

echo [4/6] 仮想環境をアクティベート中...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo エラー: 仮想環境のアクティベートに失敗しました。
    pause
    exit /b 1
)
echo 仮想環境をアクティベートしました。
echo.

echo [5/6] pipをアップグレード中...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo 警告: pipのアップグレードに失敗しましたが、続行します。
)
echo.

echo [6/6] 依存関係をインストール中...
pip install -r requirements.txt
if errorlevel 1 (
    echo エラー: 依存関係のインストールに失敗しました。
    pause
    exit /b 1
)
echo.

echo ==========================================
echo 再構築が完了しました！
echo ==========================================
echo.
echo バックエンドを起動するには、以下を実行してください:
echo   start-backend.bat
echo.
echo または、手動で起動:
echo   cd backend
echo   venv\Scripts\activate
echo   python main.py
echo.
pause
