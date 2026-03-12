@echo off
cd /d "%~dp0"
echo ========================================
echo Satellite Orbit Tracker - Run Tests
echo ========================================
echo.

pytest test_api.py test_tle.py -v

echo.
echo ========================================
echo Tests Completed
echo ========================================
pause

