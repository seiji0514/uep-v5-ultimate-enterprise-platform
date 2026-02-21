# uep-v5-ultimate-enterprise-platform を GitHub に追加するスクリプト
# 実行: PowerShell で .\scripts\add-to-github.ps1

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $repoRoot

Write-Host "=== uep-v5-ultimate-enterprise-platform を GitHub に追加 ===" -ForegroundColor Cyan

# 1. Git 初期化（未初期化の場合）
if (-not (Test-Path ".git")) {
    Write-Host "`n1. Git リポジトリを初期化..." -ForegroundColor Yellow
    git init
    git branch -M main
    Write-Host "   完了" -ForegroundColor Green
} else {
    Write-Host "`n1. Git リポジトリは既に初期化済み" -ForegroundColor Green
}

# 2. ファイルを追加
Write-Host "`n2. ファイルを追加..." -ForegroundColor Yellow
git add .
git status
Write-Host "   完了" -ForegroundColor Green

# 3. 初回コミット（未コミットの場合）
$hasCommit = git rev-parse HEAD 2>$null
if (-not $hasCommit) {
    Write-Host "`n3. 初回コミットを作成..." -ForegroundColor Yellow
    git commit -m "Initial commit: UEP v5.0 - Ultimate Enterprise Platform"
    Write-Host "   完了" -ForegroundColor Green
} else {
    Write-Host "`n3. 既存のコミットがあります。変更があればコミットしてください。" -ForegroundColor Yellow
}

# 4. リモート追加と push の案内
Write-Host "`n=== 次のステップ（手動で実行） ===" -ForegroundColor Cyan
Write-Host @"

1. GitHub でリポジトリを作成:
   https://github.com/new
   - リポジトリ名: uep-v5-ultimate-enterprise-platform
   - Public を選択
   - README 等は追加しない（既存コードを push するため）

2. 以下のコマンドを実行:

   git remote add origin https://github.com/seiji0514/uep-v5-ultimate-enterprise-platform.git
   git push -u origin main

   ※ seiji0514 はあなたの GitHub ユーザー名に置き換えてください

3. Render でリポジトリを再読み込みすると表示されます

"@ -ForegroundColor White
