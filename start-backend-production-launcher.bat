@echo off
chcp 65001 >nul
cd /d "%~dp0"
call "%~dp0本番デプロイ\start-backend-production.bat"
