# Kill processes on port 8000 and verify. Exit 0=OK, 1=still in use

$conn = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($conn) {
    $pids = $conn.OwningProcess | Sort-Object -Unique
    foreach ($procId in $pids) {
        Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
    }
    Write-Host "Port 8000 freed. Waiting for release..."
    Start-Sleep -Seconds 5
} else {
    Write-Host "Port 8000 is not in use."
}

# Retry check (port may take time to release after process kill)
$maxRetries = 3
for ($i = 1; $i -le $maxRetries; $i++) {
    Start-Sleep -Seconds 2
    $stillInUse = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
    if (-not $stillInUse) {
        Write-Host "Port 8000 is ready."
        exit 0
    }
    if ($i -lt $maxRetries) {
        Write-Host "Waiting... ($i/$maxRetries)"
    }
}

Write-Host ""
Write-Host "*** Port 8000 is still in use ***" -ForegroundColor Red
Write-Host "Run kill-port-8000.bat as Administrator, or press Ctrl+C in the other window" -ForegroundColor Yellow
exit 1
