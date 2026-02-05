@echo off
cd /d "%~dp0"
title Panaversity AI Employee launcher
color 0b

echo ========================================================
echo      Panaversity AI Employee - Autonomous System
echo ========================================================
echo.

:: 1. Cleanup First
echo [INFO] Cleaning up old processes...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM node.exe /T 2>nul
timeout /t 2 >nul

:: 2. Check for virtual environment
set "PYTHON_EXE=python"
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
    echo [INFO] Using Virtual Environment
)

:: 3. Start Watchers (Sensors)
echo [START] Launching Watchers (Email/WA)...
start "Watchers" cmd /k "%PYTHON_EXE% watchers.py"

:: 4. Start Brain Agent (Reasoning)
echo [START] Launching Brain Agent...
start "Brain Agent" cmd /k "%PYTHON_EXE% agents/brain_agent.py"

:: 5. Start Backend API
echo [START] Launching Backend API (Port 8000)...
start "Backend API" cmd /k "%PYTHON_EXE% src/api/chat_api.py"

:: Wait for backend
timeout /t 5 >nul

:: 6. Start Frontend UI
echo [START] Launching Frontend UI (Port 3000)...
cd frontend
if not exist "node_modules" call npm install
start "Frontend UI" cmd /k "npm run dev"
cd ..

echo.
echo ========================================================
echo [SUCCESS] System Started!
echo.
echo Dashboard: http://localhost:3000/dashboard
echo Chat:      http://localhost:3000
echo Status:    http://localhost:8000/api/status
echo.
echo Multiple windows have opened. Keep them open for the 24/7 AI!
echo Press any key to stop everything.
echo ========================================================
pause

taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM node.exe /T 2>nul
echo [STOPPED]
