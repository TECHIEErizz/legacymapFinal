# Start both services and keep them running
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Full-Stack Development Server" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Frontend will run on: http://localhost:3000" -ForegroundColor Yellow
Write-Host "Backend API Docs on: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "Backend API will respond on: http://localhost:8000" -ForegroundColor Yellow
Write-Host ""

# Start backend in background
Write-Host "Starting backend server..." -ForegroundColor Green
$backendPath = Join-Path $PSScriptRoot "\..\backend"
$backend = Start-Process -FilePath "python" `
    -ArgumentList "-m uvicorn app.main:app --host 0.0.0.0 --port 8000" `
    -WorkingDirectory $backendPath `
    -PassThru `
    -NoNewWindow
Write-Host "Backend started (PID: $($backend.Id))" -ForegroundColor Green

Start-Sleep -Seconds 2

# Start frontend in current window
Write-Host ""
Write-Host "Starting frontend server..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Yellow
Write-Host ""

Push-Location $PSScriptRoot
npm run dev
Pop-Location

# Cleanup - stop backend if it's still running
Write-Host "Stopping services..." -ForegroundColor Yellow
Stop-Process -Id $backend.Id -ErrorAction SilentlyContinue
Write-Host "Services stopped" -ForegroundColor Green
