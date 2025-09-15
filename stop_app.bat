@echo off
for /f "tokens=5" %%a in ('netstat -ano ^| find ":5000"') do (
    taskkill /PID %%a /F
)
echo Flask server stopped if running on port 5000.
pause
