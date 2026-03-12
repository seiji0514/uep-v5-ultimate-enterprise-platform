# 医療・ヘルスケアプラットフォーム フロントエンド起動（ポート3003）
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\frontend

if (-not (Test-Path node_modules)) {
    Write-Host "npm install を実行します..."
    npm install
}

$env:PORT = 3003
$env:REACT_APP_MEDICAL_PLATFORM_URL = "http://localhost:9003"
Write-Host "URL: http://localhost:3003"
Write-Host "バックエンド: http://localhost:9003"
npm start
