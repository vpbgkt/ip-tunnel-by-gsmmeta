@echo off
REM Quick launcher for IP Tunnel by GsmMeta

echo ============================================================
echo IP Tunnel by GsmMeta - Windows Launcher
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or later from python.org
    echo.
    pause
    exit /b 1
)

echo Python found.
echo.

REM Check if dependencies are installed
echo Checking dependencies...
python start.py
if errorlevel 1 (
    echo.
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

echo.
echo Starting IP Tunnel application...
echo.

REM Run the application
python main.py

if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)
