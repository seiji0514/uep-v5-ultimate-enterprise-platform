@echo off
chcp 65001
echo ==========================================
echo UEP v5.0 - Rebuild After Manual Delete
echo ==========================================
echo.
echo This script assumes you have manually deleted the venv folder.
echo.
pause

cd /d "%~dp0backend"
if errorlevel 1 (
    echo ERROR: Cannot access backend directory.
    pause
    exit /b 1
)

echo Checking if venv folder exists...
if exist venv (
    echo ERROR: venv folder still exists!
    echo Please delete it manually first.
    echo.
    echo Steps:
    echo   1. Close Cursor/VS Code
    echo   2. Delete: %CD%\venv
    echo   3. Run this script again
    echo.
    pause
    exit /b 1
)

echo venv folder does not exist. Good!
echo.

echo Step 1: Terminating Python processes...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul
echo Done.
echo.

echo Step 2: Creating new virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    echo Please check Python installation.
    pause
    exit /b 1
)
echo Done.
echo.

echo Step 3: Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment.
    pause
    exit /b 1
)
echo Done.
echo.

echo Step 4: Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo WARNING: Failed to upgrade pip, but continuing...
)
echo Done.
echo.

echo Step 5: Installing dependencies...
echo This will take several minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)
echo Done.
echo.

echo ==========================================
echo Rebuild completed successfully!
echo ==========================================
echo.
echo To start the backend, run: start-backend.bat
echo.
pause
