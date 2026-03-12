@echo off
cd /d "%~dp0backend"
echo Starting Enterprise Operations Hub Backend (port 9020)...
python -m uvicorn main:app --host 0.0.0.0 --port 9020 --reload
