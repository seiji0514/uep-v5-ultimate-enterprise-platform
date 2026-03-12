# 金融・FinTechプラットフォーム フロントエンド起動（ポート3004）
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\frontend

if (-not (Test-Path node_modules)) {
    Write-Host "npm install を実行します..."
    npm install
}

$env:PORT = 3004
$env:REACT_APP_FINTECH_PLATFORM_URL = "http://localhost:9004"
Write-Host "URL: http://localhost:3004"
Write-Host "バックエンド: http://localhost:9004"
npm start
