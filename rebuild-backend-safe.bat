@echo off
chcp 65001 >nul 2>&1
echo ==========================================
echo UEP v5.0 - Backend Rebuild Script (Safe Version)
echo ==========================================
echo.
echo This script rebuilds without deleting the virtual environment.
echo It will overwrite install dependencies in the existing environment.
echo.

cd /d "%~dp0backend"

REM Terminate Python processes
echo [1/4] Terminating Python processes...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul
echo Python processes terminated.
echo.

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo [2/4] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo Virtual environment created.
) else (
    echo [2/4] Using existing virtual environment.
)
echo.

REM Activate virtual environment
echo [3/4] Activating virtual environment...
if not exist venv\Scripts\activate.bat (
    echo ERROR: Virtual environment is corrupted. Recreating...
    rmdir /s /q venv >nul 2>&1
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to recreate virtual environment.
        pause
        exit /b 1
    )
)

call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment.
    echo Trying to recreate virtual environment...
    rmdir /s /q venv >nul 2>&1
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to recreate virtual environment.
        pause
        exit /b 1
    )
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo ERROR: Still failed to activate virtual environment.
        pause
        exit /b 1
    )
)
echo Virtual environment activated.
echo.

REM Upgrade pip and install dependencies
echo [4/4] Upgrading pip and installing dependencies...
python -m pip install --upgrade pip
pip install --upgrade -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)
echo.

echo ==========================================
echo Rebuild completed successfully!
echo ==========================================
echo.
echo To start the backend, run:
echo   start-backend.bat
echo.
pause
