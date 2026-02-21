@echo off
setlocal
chcp 65001
echo ==========================================
echo UEP v5.0 - Simple Backend Rebuild
echo ==========================================
echo.
echo DO NOT CLOSE THIS WINDOW!
echo.
pause

cd /d "%~dp0backend"
if errorlevel 1 (
    echo ERROR: Cannot access backend directory.
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo Step 1: Terminating Python processes...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul
echo Done.
echo.

echo Step 2: Removing virtual environment...
if exist venv (
    echo Attempting to delete venv folder...
    echo This may take a while if files are locked...
    echo.
    
    REM 複数回試行して削除
    set delete_attempts=0
    :delete_retry
    set /a delete_attempts+=1
    
    REM Pythonプロセスを終了
    taskkill /F /IM python.exe /T >nul 2>&1
    taskkill /F /IM pythonw.exe /T >nul 2>&1
    timeout /t 2 /nobreak >nul
    
    REM 属性を変更してから削除
    attrib -r -s -h venv\*.* /s /d >nul 2>&1
    
    REM Scriptsフォルダを削除
    if exist venv\Scripts (
        del /f /q venv\Scripts\*.* >nul 2>&1
        rmdir /s /q venv\Scripts >nul 2>&1
    )
    
    REM Libフォルダを削除
    if exist venv\Lib (
        if exist venv\Lib\site-packages (
            del /f /q venv\Lib\site-packages\*.* >nul 2>&1
            for /d %%d in (venv\Lib\site-packages\*) do (
                rmdir /s /q "%%d" >nul 2>&1
            )
        )
        rmdir /s /q venv\Lib >nul 2>&1
    )
    
    REM 残りを削除
    del /f /q venv\*.* >nul 2>&1
    rmdir /s /q venv >nul 2>&1
    timeout /t 2 /nobreak >nul
    
    if exist venv (
        if %delete_attempts% LSS 5 (
            echo Retry %delete_attempts%: Some files are still locked. Retrying...
            timeout /t 3 /nobreak >nul
            goto delete_retry
        ) else (
            echo WARNING: Could not completely delete venv folder.
            echo Some files may still be locked by editors or other processes.
            echo.
            echo Attempting to create virtual environment anyway...
            echo If this fails, please:
            echo   1. Close Cursor/VS Code
            echo   2. Restart your computer
            echo   3. Run this script again
            echo.
            timeout /t 3 /nobreak >nul
        )
    ) else (
        echo Successfully deleted virtual environment.
    )
) else (
    echo Virtual environment does not exist.
)
echo Done.
echo.

echo Step 3: Creating new virtual environment...
REM 既存のvenvフォルダが残っている場合は、別名で作成してから置き換え
if exist venv (
    echo WARNING: venv folder still exists. Creating temporary virtual environment...
    python -m venv venv_new
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        echo.
        echo Please manually delete the venv folder:
        echo   1. Close Cursor/VS Code
        echo   2. Delete: %CD%\venv
        echo   3. Run this script again
        echo.
        pause
        exit /b 1
    )
    echo Removing old venv folder...
    rmdir /s /q venv >nul 2>&1
    timeout /t 2 /nobreak >nul
    echo Renaming new virtual environment...
    ren venv_new venv
    if errorlevel 1 (
        echo ERROR: Failed to rename virtual environment.
        pause
        exit /b 1
    )
    echo Done.
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        echo Please check Python installation.
        pause
        exit /b 1
    )
    echo Done.
)
echo.

echo Step 4: Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment.
    pause
    exit /b 1
)
echo Done.
echo.

echo Step 5: Upgrading pip...
python -m pip install --upgrade pip
echo Done.
echo.

echo Step 6: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)
echo Done.
echo.

echo ==========================================
echo Rebuild completed!
echo ==========================================
echo.
echo To start the backend, run: start-backend.bat
echo.
pause
endlocal
