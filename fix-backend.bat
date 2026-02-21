@echo off
chcp 65001 >nul 2>&1
echo ==========================================
echo UEP v5.0 - Backend Fix Script
echo ==========================================
echo.

cd /d "%~dp0backend"

echo Step 1: Terminating Python processes...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul
echo Done.
echo.

echo Step 2: Checking virtual environment...
if not exist venv (
    echo Virtual environment not found. Creating new one...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        echo Please check Python installation.
        pause
        exit /b 1
    )
    echo Virtual environment created.
) else (
    echo Virtual environment found.
)
echo.

echo Step 3: Activating virtual environment...
if not exist venv\Scripts\activate.bat (
    echo WARNING: Virtual environment is corrupted.
    echo Attempting to recreate (this may take a moment)...
    echo.
    
    REM 複数回試行して削除
    set retry_count=0
    :retry_delete
    set /a retry_count+=1
    if %retry_count% GTR 3 (
        echo ERROR: Cannot delete corrupted virtual environment.
        echo Please manually delete backend\venv folder and run this script again.
        echo Or run as administrator.
        pause
        exit /b 1
    )
    
    timeout /t 2 /nobreak >nul
    rmdir /s /q venv >nul 2>&1
    if exist venv (
        echo Retry %retry_count%: Waiting before retry...
        goto retry_delete
    )
    
    echo Creating new virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to recreate virtual environment.
        echo Please run as administrator or manually delete backend\venv folder.
        pause
        exit /b 1
    )
    echo Virtual environment recreated successfully.
)

REM アクティベートを試行
call venv\Scripts\activate.bat >nul 2>&1
if errorlevel 1 (
    echo WARNING: Failed to activate virtual environment.
    echo Trying to use Python directly from venv...
    if exist venv\Scripts\python.exe (
        set VENV_PYTHON=venv\Scripts\python.exe
    ) else (
        echo ERROR: Cannot find Python in virtual environment.
        echo Please run rebuild-backend-simple.bat to recreate the environment.
        pause
        exit /b 1
    )
) else (
    echo Virtual environment activated.
    set VENV_PYTHON=python
)
echo.

echo Step 4: Upgrading pip...
%VENV_PYTHON% -m pip install --upgrade pip
if errorlevel 1 (
    echo WARNING: Failed to upgrade pip, but continuing...
)
echo Done.
echo.

echo Step 5: Installing missing dependencies...
echo Installing langsmith...
%VENV_PYTHON% -m pip install "langsmith>=0.0.77,<0.1.0"
echo Installing all dependencies...
%VENV_PYTHON% -m pip install -r requirements.txt
if errorlevel 1 (
    echo WARNING: Some dependencies failed to install, but continuing...
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
