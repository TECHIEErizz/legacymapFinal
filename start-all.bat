@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Starting Full-Stack Development Server
echo ========================================
echo.
echo Frontend will run on: http://localhost:3000
echo Backend API Docs on: http://localhost:8000/docs
echo Backend API will respond on: http://localhost:8000
echo.

REM Start backend in separate window
echo Starting backend server...
cd /d "%~dp0\backend"
start "Backend Server" cmd /k "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
timeout /t 2 /nobreak

REM Start frontend
cd /d "%~dp0\frontend"
echo.
echo Starting frontend server...
echo Press Ctrl+C to stop all services
echo.
npm run dev

pause
