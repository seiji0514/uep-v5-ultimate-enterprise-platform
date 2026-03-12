# UEP v5.0 - PC容量確保スクリプト
# 圧縮・削除可能な箇所を検出し、オプションで削除します
# 実行: powershell -ExecutionPolicy Bypass -File scripts\disk-space-cleanup.ps1

param(
    [switch]$DetectOnly,   # 検出のみ（削除しない）
    [switch]$Clean         # 削除を実行
)

$ErrorActionPreference = "SilentlyContinue"
$root = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
Set-Location $root

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "UEP v5.0 - PC容量確保" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 検出対象のパターン
$targets = @(
    @{ Name = "node_modules"; Path = "node_modules"; Recreate = "npm install" }
    @{ Name = "venv"; Path = "venv"; Recreate = "pip install -r requirements.txt" }
    @{ Name = "__pycache__"; Path = "__pycache__"; Recreate = "自動生成" }
    @{ Name = ".pytest_cache"; Path = ".pytest_cache"; Recreate = "自動生成" }
    @{ Name = "build"; Path = "build"; Recreate = "npm run build" }
    @{ Name = "dist"; Path = "dist"; Recreate = "再ビルド" }
    @{ Name = "htmlcov"; Path = "htmlcov"; Recreate = "pytest --cov" }
    @{ Name = ".coverage"; Path = ".coverage"; Recreate = "pytest --cov" }
    @{ Name = "coverage.xml"; Path = "coverage.xml"; Recreate = "pytest --cov" }
    @{ Name = "*.db"; Path = "*.db"; Recreate = "起動時に再作成" }
    @{ Name = "*.sqlite"; Path = "*.sqlite"; Recreate = "起動時に再作成" }
    @{ Name = "minio_data"; Path = "minio_data"; Recreate = "Docker起動時" }
    @{ Name = "postgres_data"; Path = "postgres_data"; Recreate = "Docker起動時" }
    @{ Name = "prometheus_data"; Path = "prometheus_data"; Recreate = "Docker起動時" }
    @{ Name = "grafana_data"; Path = "grafana_data"; Recreate = "Docker起動時" }
)

function Get-SizeMB {
    param([string]$path)
    if (-not (Test-Path $path)) { return 0 }
    $sum = (Get-ChildItem $path -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    return [math]::Round($sum / 1MB, 2)
}

$found = @()
$totalMB = 0

# ディレクトリ検索
$dirPatterns = @("node_modules", "venv", "__pycache__", ".pytest_cache", "build", "dist", "htmlcov", "minio_data", "postgres_data", "prometheus_data", "grafana_data")
foreach ($pattern in $dirPatterns) {
    Get-ChildItem -Path $root -Directory -Recurse -Filter $pattern -ErrorAction SilentlyContinue | ForEach-Object {
        $rel = $_.FullName.Replace($root + "\", "")
        $size = Get-SizeMB $_.FullName
        if ($size -gt 0) {
            $found += [PSCustomObject]@{ Type = "Dir"; Path = $rel; SizeMB = $size; Recreate = "再生成可能" }
            $totalMB += $size
        }
    }
}

# ファイル検索
$filePatterns = @(".coverage", "coverage.xml")
foreach ($pattern in $filePatterns) {
    Get-ChildItem -Path $root -File -Recurse -Filter $pattern -ErrorAction SilentlyContinue | ForEach-Object {
        $rel = $_.FullName.Replace($root + "\", "")
        $size = [math]::Round($_.Length / 1MB, 2)
        if ($size -gt 0) {
            $found += [PSCustomObject]@{ Type = "File"; Path = $rel; SizeMB = $size; Recreate = "再生成可能" }
            $totalMB += $size
        }
    }
}

# *.db, *.sqlite
Get-ChildItem -Path $root -File -Recurse -Include "*.db", "*.sqlite", "*.sqlite3" -ErrorAction SilentlyContinue | ForEach-Object {
    $rel = $_.FullName.Replace($root + "\", "")
    $size = [math]::Round($_.Length / 1MB, 2)
    $found += [PSCustomObject]@{ Type = "File"; Path = $rel; SizeMB = $size; Recreate = "起動時に再作成" }
    $totalMB += $size
}

# 結果表示
if ($found.Count -eq 0) {
    Write-Host "削除可能な大きなファイル・フォルダは検出されませんでした。" -ForegroundColor Yellow
    Write-Host "（node_modules, venv 等が未作成の可能性があります）" -ForegroundColor Gray
    exit 0
}

$found = $found | Sort-Object SizeMB -Descending
Write-Host "検出結果（合計: $([math]::Round($totalMB, 1)) MB）:" -ForegroundColor Green
Write-Host ""
$found | Format-Table Path, SizeMB, Recreate -AutoSize

if ($DetectOnly) {
    Write-Host "検出のみ実行しました。削除するには -Clean を指定してください。" -ForegroundColor Yellow
    exit 0
}

if (-not $Clean) {
    Write-Host ""
    Write-Host "削除を実行するには:" -ForegroundColor Yellow
    Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\disk-space-cleanup.ps1 -Clean" -ForegroundColor White
    Write-Host ""
    Write-Host "注意: node_modules, venv 削除後は npm install / pip install が必要です。" -ForegroundColor Gray
    exit 0
}

# 削除実行
Write-Host ""
$confirm = Read-Host "上記を削除しますか？ (y/N)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "キャンセルしました。" -ForegroundColor Gray
    exit 0
}

$freed = 0
foreach ($item in $found) {
    $fullPath = Join-Path $root $item.Path
    try {
        if (Test-Path $fullPath) {
            Remove-Item $fullPath -Recurse -Force -ErrorAction Stop
            Write-Host "[削除] $($item.Path) ($($item.SizeMB) MB)" -ForegroundColor Green
            $freed += $item.SizeMB
        }
    } catch {
        Write-Host "[スキップ] $($item.Path) - $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "約 $([math]::Round($freed, 1)) MB を解放しました。" -ForegroundColor Cyan
Write-Host ""
Write-Host "次のステップ:" -ForegroundColor Yellow
Write-Host "  - node_modules を削除した場合: cd frontend && npm install" -ForegroundColor White
Write-Host "  - venv を削除した場合: start-backend.bat で再作成" -ForegroundColor White
Write-Host "  - DB を削除した場合: 起動時に再作成されます（サンプルデータは再投入）" -ForegroundColor White
