# デプロイ前準備スクリプト（Windows PowerShell）
# SECRET_KEY 生成、.env テンプレート作成

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "=== UEP v5.0 デプロイ前準備 ===" -ForegroundColor Cyan

# SECRET_KEY 生成（32バイト = 64文字の16進数）
$bytes = New-Object byte[] 32
[System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
$SECRET_KEY = [BitConverter]::ToString($bytes).Replace("-", "").ToLower()

Write-Host "SECRET_KEY を生成しました" -ForegroundColor Green

# backend/.env
$backendEnv = Join-Path $ProjectRoot "backend\.env"
if (-not (Test-Path $backendEnv)) {
    @"
# 本番用（prepare-env.ps1 で生成）
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=$SECRET_KEY

# 以下を本番ドメインに変更してください
DATABASE_URL=postgresql://user:password@host:5432/uep_db
REDIS_URL=redis://:password@host:6379/0
CORS_ORIGINS=https://your-domain.com,https://industry.your-domain.com
LOG_LEVEL=WARNING
"@ | Out-File -FilePath $backendEnv -Encoding utf8
    Write-Host "backend/.env を作成しました" -ForegroundColor Green
} else {
    Write-Host "backend/.env は既に存在します" -ForegroundColor Yellow
    Write-Host "生成された SECRET_KEY: $SECRET_KEY"
}

# 本番ユーザー永続化用
$dataDir = Join-Path $ProjectRoot "backend\data"
if (-not (Test-Path $dataDir)) {
    New-Item -ItemType Directory -Path $dataDir | Out-Null
    Write-Host "backend/data/ を用意しました" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== 次のステップ ===" -ForegroundColor Cyan
Write-Host "1. backend/.env の DATABASE_URL, CORS_ORIGINS を本番用に編集"
Write-Host "2. frontend/.env.production を作成（REACT_APP_API_URL, REACT_APP_INDUSTRY_UNIFIED_URL）"
Write-Host "3. industry_unified_platform/frontend/.env.production を作成（REACT_APP_INDUSTRY_API_URL）"
Write-Host "4. deploy/nginx-ssl.conf.example を参考に nginx を設定"
Write-Host "5. scripts/register_production_user.py で本番ユーザーを登録"
