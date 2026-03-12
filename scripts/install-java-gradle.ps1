# Java 17 と Gradle インストール（管理者権限で実行）
# 使い方: 管理者として PowerShell を開き、.\scripts\install-java-gradle.ps1 を実行

Write-Host "Java 17 と Gradle を Chocolatey でインストールします..." -ForegroundColor Cyan

if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Chocolatey がインストールされていません。先に Chocolatey をインストールしてください。" -ForegroundColor Red
    exit 1
}

Write-Host "`n[1/2] Java 17 (Temurin) をインストール..." -ForegroundColor Yellow
choco install temurin17 -y

Write-Host "`n[2/2] Gradle をインストール..." -ForegroundColor Yellow
choco install gradle -y

Write-Host "`n完了。新しいターミナルを開いて以下で確認:" -ForegroundColor Green
Write-Host "  java -version"
Write-Host "  gradle -v"
