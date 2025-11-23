@echo off
cd /d "%~dp0"

echo.
echo ======================================================
echo   FULL-STACK APPLICATION - DEVELOPMENT SERVER
echo ======================================================
echo.
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop all services
echo ======================================================
echo.

REM Start backend in separate window
echo Starting Backend Server...
start "Backend" cmd /k "cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

REM Wait for backend to start
timeout /t 3 /nobreak

REM Start frontend
echo Starting Frontend Server...
cd frontend
npm run dev

pause
