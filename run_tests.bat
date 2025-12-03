@echo off
REM Test script for PDF Receipt Processing API
REM This script runs the test suite

echo ========================================
echo  PDF Receipt API Test Suite
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Make sure the API is running in another terminal!
echo Run: start_api.bat
echo.
echo Press any key to continue with testing...
pause

echo.
echo Running test suite...
echo.

python test_api.py

pause
