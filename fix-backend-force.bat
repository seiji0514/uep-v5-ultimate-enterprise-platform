@echo off
chcp 65001 >nul 2>&1
echo ==========================================
echo UEP v5.0 - Force Fix Backend (No Delete)
echo ==========================================
echo.
echo This script fixes dependencies WITHOUT deleting the virtual environment.
echo Use this if you get "Permission denied" errors.
echo.

cd /d "%~dp0backend"

echo Step 1: Terminating Python processes...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 3 /nobreak >nul
echo Done.
echo.

echo Step 2: Checking Python executable...
if exist venv\Scripts\python.exe (
    set VENV_PYTHON=venv\Scripts\python.exe
    echo Found Python in virtual environment.
) else if exist venv\Scripts\pythonw.exe (
    set VENV_PYTHON=venv\Scripts\pythonw.exe
    echo Found Pythonw in virtual environment.
) else (
    echo ERROR: Cannot find Python executable in virtual environment.
    echo Please run rebuild-backend-simple.bat to recreate the environment.
    pause
    exit /b 1
)
echo.

echo Step 3: Upgrading pip...
%VENV_PYTHON% -m pip install --upgrade pip --quiet
echo Done.
echo.

echo Step 4: Installing langsmith...
%VENV_PYTHON% -m pip install "langsmith>=0.0.77,<0.1.0" --quiet
echo Done.
echo.

echo Step 5: Installing/upgrading all dependencies...
%VENV_PYTHON% -m pip install --upgrade -r requirements.txt
if errorlevel 1 (
    echo WARNING: Some dependencies failed, but continuing...
)
echo Done.
echo.

echo ==========================================
echo Fix completed!
echo ==========================================
echo.
echo To start the backend, run: start-backend.bat
echo.
pause
