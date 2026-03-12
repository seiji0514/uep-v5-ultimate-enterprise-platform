# .sh の CRLF を LF に変換
$dir = Join-Path $PSScriptRoot "projects\unified-platform\scripts"
Get-ChildItem $dir -Filter "*.sh" | ForEach-Object {
    $c = [System.IO.File]::ReadAllText($_.FullName) -replace "`r`n", "`n" -replace "`r", "`n"
    [System.IO.File]::WriteAllText($_.FullName, $c)
    Write-Host "Fixed: $($_.Name)"
}
