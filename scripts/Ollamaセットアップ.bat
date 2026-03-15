@echo off
chcp 65001 >nul
echo ========================================
echo Ollama セットアップ（VS Code + Continue用）
echo ========================================
echo.

where ollama >nul 2>&1
if %errorlevel% neq 0 (
    echo [エラー] Ollama がインストールされていません。
    echo https://ollama.ai からダウンロードしてインストールしてください。
    pause
    exit /b 1
)

echo [1/3] Ollama のバージョン確認...
ollama --version
echo.

echo [2/3] 推奨モデルをダウンロード中...
echo 軽量モデル: deepseek-coder:6.7b （約4GB）
ollama pull deepseek-coder:6.7b
if %errorlevel% neq 0 (
    echo ダウンロードに失敗しました。ネットワーク接続を確認してください。
    pause
    exit /b 1
)

echo.
echo [3/3] インストール済みモデル一覧
ollama list
echo.

echo ========================================
echo セットアップ完了
echo ========================================
echo.
echo 次のステップ:
echo 1. VS Code で Continue 拡張機能をインストール
echo 2. プロジェクトの .continue/config.yaml を確認
echo 3. Ctrl+L で Continue チャットを開いて動作確認
echo.
echo 詳細は docs\セットアップ_VSCode_Continue_Ollama.md を参照
echo.
pause
