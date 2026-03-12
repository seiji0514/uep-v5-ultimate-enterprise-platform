# 製造・IoTプラットフォーム フロントエンド起動（ポート3002）
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\frontend

if (-not (Test-Path node_modules)) {
    Write-Host "npm install を実行します..."
    npm install
}

$env:PORT = 3002
$env:REACT_APP_MANUFACTURING_PLATFORM_URL = "http://localhost:9002"
Write-Host "URL: http://localhost:3002"
Write-Host "バックエンド: http://localhost:9002"
npm start
