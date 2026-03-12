# 産業統合プラットフォーム フロントエンド起動（ポート3010）
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\frontend

if (-not (Test-Path node_modules)) {
    Write-Host "npm install を実行します..."
    npm install
}

$env:PORT = 3010
$env:REACT_APP_INDUSTRY_API_URL = "http://localhost:9010"
Write-Host "URL: http://localhost:3010"
Write-Host "バックエンド: http://localhost:9010"
npm start
