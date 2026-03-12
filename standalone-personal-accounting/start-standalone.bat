@echo off
chcp 65001 >nul
echo ==========================================
echo Personal Accounting - Standalone
echo ==========================================
echo.

cd /d "%~dp0"

REM Backend
start "PersonalAccounting-API" cmd /k "cd /d %~dp0backend && pip install -r requirements.txt -q && python main.py"

REM Wait for backend
timeout /t 3 /nobreak >nul

REM Frontend
start "PersonalAccounting-Front" cmd /k "cd /d %~dp0frontend && python -m http.server 3001"

echo.
echo Started.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3001
echo API Docs: http://localhost:5000/docs
echo.
echo Open http://localhost:3001 in your browser.
echo.
pause
