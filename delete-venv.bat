@echo off
setlocal enabledelayedexpansion
chcp 65001

echo ==========================================
echo UEP v5.0 - Delete Virtual Environment
echo ==========================================
echo.
echo This script will forcefully delete the virtual environment.
echo It will attempt multiple times even if files are locked.
echo.
echo DO NOT CLOSE THIS WINDOW!
echo.
pause
if errorlevel 1 (
    echo User cancelled.
    pause
    exit /b 0
)

echo.
echo Checking project directory...
cd /d "%~dp0"
if errorlevel 1 (
    echo ERROR: Cannot access project directory.
    pause
    exit /b 1
)
echo Current directory: %CD%
echo.

cd backend
if errorlevel 1 (
    echo ERROR: Cannot access backend directory.
    echo Please make sure you are running this from the project root.
    pause
    exit /b 1
)
echo Backend directory: %CD%
echo.

echo Step 1: Terminating all Python processes...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1
timeout /t 3 /nobreak >nul
if errorlevel 1 (
    echo WARNING: Some Python processes may still be running.
) else (
    echo Done.
)
echo.

echo Step 2: Checking virtual environment...
if not exist venv (
    echo Virtual environment does not exist.
    echo Skipping deletion and proceeding to rebuild...
    echo.
    goto rebuild
)
echo Virtual environment found. Proceeding with deletion...
echo.

echo Attempting to delete venv folder...
echo This may take a few moments...
echo.

REM 複数回試行（エディタが開いていても削除を試みる）
set attempts=0
:delete_loop
set /a attempts+=1
echo.
echo ==========================================
echo Attempt %attempts%: Deleting venv folder...
echo ==========================================
echo This may take a while if files are locked...
echo Do not close this window!
echo.

REM より長い待機時間を設定
if %attempts% EQU 1 (
    echo Please wait, this may take several minutes...
    echo.
)
timeout /t 3 /nobreak >nul

REM 属性を変更してから削除（読み取り専用を解除）
attrib -r -s -h venv\*.* /s /d >nul 2>&1
timeout /t 2 /nobreak >nul

REM Scriptsフォルダ内のファイルを個別に削除
if exist venv\Scripts (
    echo Deleting Scripts folder...
    del /f /q venv\Scripts\*.* >nul 2>&1
    timeout /t 2 /nobreak >nul
    rmdir /s /q venv\Scripts >nul 2>&1
    timeout /t 2 /nobreak >nul
)

REM Libフォルダ内のファイルを段階的に削除
if exist venv\Lib (
    echo Deleting Lib folder (this may take time)...
    REM site-packagesを先に削除
    if exist venv\Lib\site-packages (
        del /f /q venv\Lib\site-packages\*.* >nul 2>&1
        for /d %%d in (venv\Lib\site-packages\*) do (
            rmdir /s /q "%%d" >nul 2>&1
        )
        timeout /t 2 /nobreak >nul
    )
    rmdir /s /q venv\Lib >nul 2>&1
    timeout /t 2 /nobreak >nul
)

REM 残りのファイルを削除
if exist venv (
    echo Deleting remaining files...
    del /f /q venv\*.* >nul 2>&1
    for /d %%d in (venv\*) do (
        if /i not "%%~nxd"=="Scripts" if /i not "%%~nxd"=="Lib" (
            rmdir /s /q "%%d" >nul 2>&1
        )
    )
    timeout /t 3 /nobreak >nul
    rmdir /s /q venv >nul 2>&1
    timeout /t 2 /nobreak >nul
)

if exist venv (
    if %attempts% LSS 10 (
        echo Failed. Waiting longer and retrying...
        timeout /t 5 /nobreak >nul
        goto delete_loop
    ) else (
        echo.
        echo WARNING: Could not completely delete venv folder after 10 attempts.
        echo Some files may still be locked by editors or other processes.
        echo.
        echo The virtual environment may be partially deleted.
        echo You can try:
        echo   1. Close Cursor/VS Code and run this script again
        echo   2. Restart your computer and run rebuild-backend-simple.bat
        echo   3. Manually delete the remaining files in File Explorer
        echo.
        echo Continuing with rebuild anyway...
        echo.
        timeout /t 3 /nobreak >nul
    )
) else (
    echo.
    echo Successfully deleted virtual environment!
    echo.
)

:rebuild
echo ==========================================
echo Step 3: Rebuilding virtual environment...
echo ==========================================
echo.
echo Now running rebuild-backend-simple.bat...
echo This will create a new virtual environment and install dependencies.
echo Please wait...
echo.
timeout /t 2 /nobreak >nul

REM 自動的に再構築スクリプトを実行
cd /d "%~dp0"
if errorlevel 1 (
    echo ERROR: Cannot return to project root directory.
    echo Current directory: %CD%
    echo Please run rebuild-backend-simple.bat manually.
    pause
    exit /b 1
)

echo Project root directory: %CD%
if exist rebuild-backend-simple.bat (
    echo Found rebuild-backend-simple.bat
    echo.
    echo ==========================================
    echo Starting rebuild process...
    echo ==========================================
    echo.
    call rebuild-backend-simple.bat
    set rebuild_error=!errorlevel!
    if !rebuild_error! NEQ 0 (
        echo.
        echo ERROR: Rebuild failed with error code: !rebuild_error!
        echo Please check the error messages above.
        pause
        exit /b 1
    )
) else (
    echo ERROR: rebuild-backend-simple.bat not found!
    echo Current directory: %CD%
    echo Please run it manually.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo All done!
echo ==========================================
echo.
echo To start the backend, run: start-backend.bat
echo.
pause
endlocal
