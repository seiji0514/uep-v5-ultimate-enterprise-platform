# UEP v5.0 - フロントエンド起動（PowerShell用）
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "=========================================="
Write-Host "UEP v5.0 - フロントエンド起動"
Write-Host "=========================================="
Write-Host ""

if (-not (Test-Path "frontend")) {
    Write-Host "[エラー] frontend ディレクトリが見つかりません" -ForegroundColor Red
    exit 1
}

Set-Location frontend

if (-not (Test-Path "package.json")) {
    Write-Host "[エラー] package.json が見つかりません" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "node_modules")) {
    Write-Host "依存パッケージをインストール中..."
    npm install
}

# .envが無ければ.exampleから作成
if (-not (Test-Path ".env") -and (Test-Path ".env.example")) {
    Write-Host ".env を作成中（.env.example からコピー）..."
    Copy-Item ".env.example" ".env"
}

# UEP→EOHリンク用（.envに無い場合のフォールバック）
if (-not $env:REACT_APP_EOH_URL) { $env:REACT_APP_EOH_URL = "http://localhost:3020" }

Write-Host ""
Write-Host "フロントエンドを起動中..."
Write-Host "URL: http://localhost:3000"
Write-Host "停止: Ctrl+C"
Write-Host ""

npm start
