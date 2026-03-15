@echo off
chcp 65001 >nul
REM UEP v5.0 本体の DB バックアップ（SQLite / PostgreSQL 対応）
REM 定期実行: タスクスケジューラで日次実行を設定
REM 例: 毎日 2:00 に実行

setlocal
cd /d "%~dp0.."
set ROOT=%CD%
set BACKUP_DIR=%ROOT%\backups\db
set DATE=%date:~0,4%-%date:~5,2%-%date:~8,2%
set TIME=%time:~0,2%%time:~3,2%%time:~6,2%
set TIME=%TIME: =0%

if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"
if not exist "%BACKUP_DIR%\%DATE%" mkdir "%BACKUP_DIR%\%DATE%"

REM SQLite の場合（backend/uep_db.sqlite または backend のカレントで uep_db.sqlite）
set SQLITE_PATH=%ROOT%\backend\uep_db.sqlite
if not exist "%SQLITE_PATH%" set SQLITE_PATH=%ROOT%\uep_db.sqlite
if exist "%SQLITE_PATH%" (
    echo [SQLite] %SQLITE_PATH% をバックアップ中...
    copy "%SQLITE_PATH%" "%BACKUP_DIR%\%DATE%\uep_db_%DATE%_%TIME%.sqlite" >nul
    echo [完了] %BACKUP_DIR%\%DATE%\uep_db_%DATE%_%TIME%.sqlite
    goto :end
)

REM PostgreSQL の場合（DATABASE_URL が postgresql:// の場合）
REM 環境に pg_dump がある場合のみ。未設定ならスキップ
where pg_dump >nul 2>&1
if %errorlevel% equ 0 (
    if defined DATABASE_URL (
        echo [PostgreSQL] pg_dump でバックアップ中...
        set OUT=%BACKUP_DIR%\%DATE%\uep_db_%DATE%_%TIME%.sql
        pg_dump %DATABASE_URL% > "%OUT%" 2>nul
        if exist "%OUT%" echo [完了] %OUT%
    )
)

:end
endlocal
