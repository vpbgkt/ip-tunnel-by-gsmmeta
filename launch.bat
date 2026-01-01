@echo off
REM IP Tunnel by GsmMeta - Desktop Launcher
REM Place this in the project folder or create a shortcut to it

cd /d "%~dp0"

REM Set window title
title IP Tunnel by GsmMeta

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    echo.
    echo Please install Python from https://www.python.org
    echo.
    pause
    exit /b 1
)

REM Run the application
python main.py

REM If there was an error, pause to see it
if errorlevel 1 (
    echo.
    echo Application encountered an error.
    pause
)
