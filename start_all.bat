@echo off
echo ========================================
echo  Social Media Platform - Startup Script
echo ========================================
echo.
echo This will start all three services:
echo 1. Backend API (Port 8000)
echo 2. Frontend (Port 3000)
echo 3. Sentiment Analysis API (Port 8001)
echo.
echo Press Ctrl+C in any window to stop that service
echo.
pause

echo Starting Backend...
start "Backend API (Port 8000)" cmd /k "cd social-media-platform\backend && venv\Scripts\activate && echo Backend starting... && uvicorn app.main:app --reload --port 8000"

echo Waiting 3 seconds...
timeout /t 3 /nobreak > nul

echo Starting Frontend...
start "Frontend (Port 3000)" cmd /k "cd social-media-platform\frontend && echo Frontend starting... && npm run dev"

echo Waiting 3 seconds...
timeout /t 3 /nobreak > nul

echo Starting Sentiment Analysis...
start "Sentiment API (Port 8001)" cmd /k "cd sentiment-analysis-engine && venv\Scripts\activate && echo Sentiment API starting... && uvicorn app.main:app --reload --port 8001"

echo.
echo ========================================
echo All services are starting!
echo ========================================
echo.
echo URLs:
echo Frontend:     http://localhost:3000
echo Backend API:  http://localhost:8000/docs
echo Sentiment:    http://localhost:8001/docs
echo.
echo Three new windows should have opened.
echo Check each window for any errors.
echo.
echo Press any key to exit this window...
pause > nul
