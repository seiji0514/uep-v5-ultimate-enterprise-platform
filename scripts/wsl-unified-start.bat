@echo off
chcp 65001 >nul
REM WSL: Docker + Unified Platform 一括起動
cd /d "%~dp0.."
for /f "delims=" %%i in ('wsl wslpath -u "%CD%" 2^>nul') do set "WSL_ROOT=%%i"
if not defined WSL_ROOT set "WSL_ROOT=/mnt/c/uep-v5-ultimate-enterprise-platform"
wsl -e bash -c "cd '%WSL_ROOT%/projects/unified-platform' && bash scripts/wsl-start-all.sh"
pause
