@echo off
chcp 65001 >nul
echo ==========================================
echo Personal Accounting - PRACTICE MODE
echo ==========================================
echo.

cd /d "%~dp0"

REM Backend (練習モード・ポート5001で本番と競合しない)
start "PersonalAccounting-API-Practice" cmd /k "cd /d %~dp0backend && pip install -r requirements.txt -q && run-practice.bat"

REM Wait for backend
timeout /t 3 /nobreak >nul

REM Frontend (ポート3010で本番・他システムと競合しない)
start "PersonalAccounting-Front-Practice" cmd /k "cd /d %~dp0frontend && python -m http.server 3010"

echo.
echo Started (PRACTICE MODE).
echo Backend:  http://localhost:5001
echo Frontend: http://localhost:3010
echo.
echo Open http://localhost:3010 in your browser.
echo.
pause
