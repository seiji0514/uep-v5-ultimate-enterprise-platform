@echo off
cd /d "%~dp0frontend"
if not exist node_modules npm install
set PORT=3020
set REACT_APP_EOH_API_URL=http://localhost:9020
echo Starting Enterprise Operations Hub Frontend (port 3020)...
npm start
