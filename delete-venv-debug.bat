@echo off
setlocal enabledelayedexpansion
chcp 65001

echo ==========================================
echo UEP v5.0 - Delete Virtual Environment (DEBUG)
echo ==========================================
echo.
echo This is a debug version that will show all errors.
echo.
pause

echo.
echo [DEBUG] Script started
echo [DEBUG] Current directory: %CD%
echo [DEBUG] Script location: %~dp0
echo.

REM プロジェクトルートに移動
cd /d "%~dp0"
if errorlevel 1 (
    echo [ERROR] Cannot change to script directory: %~dp0
    echo [ERROR] Error level: %errorlevel%
    pause
    exit /b 1
)
echo [DEBUG] Changed to project root: %CD%

REM バックエンドディレクトリに移動
if not exist "backend" (
    echo [ERROR] backend directory does not exist!
    echo [ERROR] Current directory: %CD%
    echo [ERROR] Expected: %CD%\backend
    dir
    pause
    exit /b 1
)

cd backend
if errorlevel 1 (
    echo [ERROR] Cannot change to backend directory
    echo [ERROR] Error level: %errorlevel%
    pause
    exit /b 1
)
echo [DEBUG] Changed to backend directory: %CD%
echo.

echo Step 1: Terminating Python processes...
taskkill /F /IM python.exe /T
if errorlevel 1 (
    echo [DEBUG] No python.exe processes found or error occurred
) else (
    echo [DEBUG] Python processes terminated
)
taskkill /F /IM pythonw.exe /T
if errorlevel 1 (
    echo [DEBUG] No pythonw.exe processes found or error occurred
) else (
    echo [DEBUG] Pythonw processes terminated
)
timeout /t 3 /nobreak
echo Done.
echo.

echo Step 2: Checking virtual environment...
if not exist venv (
    echo Virtual environment does not exist.
    echo Skipping deletion and proceeding to rebuild...
    echo.
    goto rebuild
)
echo Virtual environment found: %CD%\venv
echo.

echo Attempting to delete venv folder...
echo This may take a few moments...
echo.

REM 複数回試行
set attempts=0
:delete_loop
set /a attempts+=1
echo.
echo ==========================================
echo Attempt %attempts%: Deleting venv folder...
echo ==========================================
echo.

if %attempts% EQU 1 (
    echo Please wait, this may take several minutes...
    echo.
)
timeout /t 3 /nobreak

REM 属性を変更
echo [DEBUG] Removing file attributes...
attrib -r -s -h venv\*.* /s /d
timeout /t 2 /nobreak

REM Scriptsフォルダを削除
if exist venv\Scripts (
    echo [DEBUG] Deleting Scripts folder...
    del /f /q venv\Scripts\*.*
    if errorlevel 1 (
        echo [WARNING] Some files in Scripts could not be deleted
    )
    timeout /t 2 /nobreak
    rmdir /s /q venv\Scripts
    if errorlevel 1 (
        echo [WARNING] Scripts folder could not be deleted
    ) else (
        echo [DEBUG] Scripts folder deleted
    )
    timeout /t 2 /nobreak
)

REM Libフォルダを削除
if exist venv\Lib (
    echo [DEBUG] Deleting Lib folder...
    if exist venv\Lib\site-packages (
        echo [DEBUG] Deleting site-packages...
        del /f /q venv\Lib\site-packages\*.*
        for /d %%d in (venv\Lib\site-packages\*) do (
            echo [DEBUG] Deleting package: %%d
            rmdir /s /q "%%d"
        )
        timeout /t 2 /nobreak
    )
    rmdir /s /q venv\Lib
    if errorlevel 1 (
        echo [WARNING] Lib folder could not be deleted
    ) else (
        echo [DEBUG] Lib folder deleted
    )
    timeout /t 2 /nobreak
)

REM 残りのファイルを削除
if exist venv (
    echo [DEBUG] Deleting remaining files...
    del /f /q venv\*.*
    for /d %%d in (venv\*) do (
        if /i not "%%~nxd"=="Scripts" if /i not "%%~nxd"=="Lib" (
            echo [DEBUG] Deleting: %%d
            rmdir /s /q "%%d"
        )
    )
    timeout /t 3 /nobreak
    rmdir /s /q venv
    timeout /t 2 /nobreak
)

if exist venv (
    if %attempts% LSS 5 (
        echo [DEBUG] Failed. Retrying...
        timeout /t 5 /nobreak
        goto delete_loop
    ) else (
        echo.
        echo WARNING: Could not completely delete venv folder after 5 attempts.
        echo Some files may still be locked.
        echo Continuing with rebuild anyway...
        echo.
        timeout /t 3 /nobreak
    )
) else (
    echo.
    echo [DEBUG] Successfully deleted virtual environment!
    echo.
)

:rebuild
echo ==========================================
echo Step 3: Rebuilding virtual environment...
echo ==========================================
echo.

cd /d "%~dp0"
if errorlevel 1 (
    echo [ERROR] Cannot return to project root
    echo [ERROR] Current directory: %CD%
    pause
    exit /b 1
)
echo [DEBUG] Returned to project root: %CD%

if not exist rebuild-backend-simple.bat (
    echo [ERROR] rebuild-backend-simple.bat not found!
    echo [ERROR] Current directory: %CD%
    dir *.bat
    pause
    exit /b 1
)

echo [DEBUG] Found rebuild-backend-simple.bat
echo Starting rebuild process...
echo.
timeout /t 2 /nobreak

call rebuild-backend-simple.bat
set rebuild_error=!errorlevel!
if !rebuild_error! NEQ 0 (
    echo.
    echo [ERROR] Rebuild failed with error code: !rebuild_error!
    pause
    exit /b 1
)

echo.
echo ==========================================
echo All done!
echo ==========================================
echo.
pause
endlocal
