@echo off
chcp 65001 >nul
echo ========================================
echo VS Code + Continue + Ollama セットアップ
echo ========================================
echo.

echo [1] Ollama のモデルをダウンロード中...
call ollama pull deepseek-coder:6.7b
if %errorlevel% neq 0 (
    echo.
    echo ※ Ollama が未インストールの場合:
    echo   PowerShell で以下を実行: irm https://ollama.com/install.ps1 ^| iex
    echo   完了後、新しいターミナルを開いてこのスクリプトを再実行
    echo.
    pause
    exit /b 1
)

echo.
echo [2] インストール済みモデル一覧
ollama list
echo.

echo [3] VS Code でプロジェクトを開いています...
start "" "C:\Users\kaho0\AppData\Local\Programs\Microsoft VS Code\Code.exe" "%~dp0.."
echo.

echo ========================================
echo 次の手順（VS Code 内で）
echo ========================================
echo 1. 拡張機能パネル（Ctrl+Shift+X）を開く
echo 2. 「Continue」で検索してインストール
echo 3. Ctrl+L で Continue チャットを開く
echo 4. モデルに「DeepSeek Coder」を選択
echo.
pause
