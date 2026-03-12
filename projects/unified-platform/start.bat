@echo off
REM UEP Standalone 統合起動スクリプト (Windows)
REM 用法: start.bat [モード...]
REM   モード: default ^| monitoring ^| redundant

cd /d "%~dp0"

set MONITORING=
set REDUNDANT=

:parse
if "%~1"=="" goto run
if "%~1"=="monitoring" set MONITORING=1
if "%~1"=="redundant" set REDUNDANT=1
if "%~1"=="default" goto next
if not "%~1"=="monitoring" if not "%~1"=="redundant" (
  echo 未知のモード: %~1 ^(default^|monitoring^|redundant^)
  exit /b 1
)
:next
shift
goto parse

:run
set PROFILES=
if defined REDUNDANT (
  echo 冗長構成で起動...
  set "COMPOSE_FILES=-f docker-compose.yml -f docker-compose.redundant.yml"
  set "PROFILES=--profile redundant"
) else (
  echo 通常起動...
  set "COMPOSE_FILES=-f docker-compose.yml"
)
if defined MONITORING (
  echo 監視付き
  set "PROFILES=%PROFILES% --profile monitoring"
)

docker compose %COMPOSE_FILES% down 2>nul
docker compose %COMPOSE_FILES% up -d --build %PROFILES%
