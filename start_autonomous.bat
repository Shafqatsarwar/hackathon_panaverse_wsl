@echo off
cd /d "%~dp0"
title Panaversity Autonomous System
color 0a

:: Force UTF-8 for Python to avoid UnicodeEncodeErrors on Windows
set PYTHONUTF8=1

echo ========================================================
echo   Panaversity AI Employee - Autonomous Mode
echo ========================================================
echo.

:: 1. Cleanup
echo [INFO] Cleaning up old processes...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM node.exe /T 2>nul
timeout /t 2 >nul

:: 2. Determine Python
set "PYTHON_EXE=python"
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
)

:: 3. Start Processes
echo [START] Watchers (Sensors)...
start "Watchers" cmd /k "%PYTHON_EXE% watchers.py"

echo [START] Brain Agent (Reasoning)...
start "Brain Agent" cmd /k "%PYTHON_EXE% agents/brain_agent.py"

echo [START] Backend API...
start "Backend API" cmd /k "%PYTHON_EXE% src/api/chat_api.py"

echo [START] Frontend UI...
cd frontend
if not exist "node_modules" call npm install
start "Frontend UI" cmd /k "npm run dev"
cd ..

echo.
echo [SUCCESS] Autonomous System Running!
echo Dashboard: http://localhost:3000/dashboard
echo Chat:      http://localhost:3000
echo.
pause
