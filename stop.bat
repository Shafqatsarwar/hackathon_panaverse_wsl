@echo off
title Stopping Panaversity Assistant
echo [INFO] Stopping all AI Employee processes...

:: Terminate Python processes (Backends, Agents, Watchers)
taskkill /F /IM python.exe /T 2>nul

:: Terminate Node processes (Frontend dev server)
taskkill /F /IM node.exe /T 2>nul

echo [SUCCESS] All processes stopped.
timeout /t 3
