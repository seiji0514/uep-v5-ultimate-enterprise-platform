# 統合セキュリティ・防衛プラットフォーム - フロントエンド起動（ポート3001）
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "=========================================="
Write-Host "統合セキュリティ・防衛プラットフォーム フロントエンド"
Write-Host "ポート3001"
Write-Host "=========================================="
Write-Host ""

Set-Location frontend

if (-not (Test-Path "package.json")) {
    Write-Host "[エラー] package.json が見つかりません" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "node_modules")) {
    Write-Host "依存パッケージをインストール中..."
    npm install
}

Write-Host ""
Write-Host "URL: http://localhost:3001"
Write-Host "バックエンド（ポート9001）を先に起動してください"
Write-Host "停止: Ctrl+C"
Write-Host ""

npm start
