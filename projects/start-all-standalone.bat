@echo off
chcp 65001 >nul
REM Medical / Aviation / Space standalone (UEP v5.0 independent)
cd /d "%~dp0"

echo [Medical] port 8001 starting...
start "medical-standalone" cmd /k "cd medical-standalone && pip install -r requirements.txt -q && python main.py"

timeout /t 2 /nobreak >nul

echo [Aviation] port 8002 starting...
start "aviation-standalone" cmd /k "cd aviation-standalone && pip install -r requirements.txt -q && python main.py"

timeout /t 2 /nobreak >nul

echo [Space] port 8003 starting...
start "space-standalone" cmd /k "cd space-standalone && pip install -r requirements.txt -q && python main.py"

echo.
echo Done. Press Ctrl+C in each window to stop.
echo Medical: http://localhost:8001/dashboard
echo Aviation: http://localhost:8002/dashboard
echo Space: http://localhost:8003/dashboard
pause
