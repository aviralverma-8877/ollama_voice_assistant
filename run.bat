@echo off
REM ============================================================================
REM Ollama Voice Assistant - Quick Launch Script
REM ============================================================================
REM Use this script for quick launches after initial deployment
REM If this is your first time, run deploy.bat instead
REM ============================================================================

echo.
echo ======================================================================
echo   OLLAMA VOICE ASSISTANT - QUICK LAUNCH
echo ======================================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please run deploy.bat first to set up the environment.
    echo.
    pause
    exit /b 1
)

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    echo.
    echo Try running deploy.bat again to fix the environment.
    echo.
    pause
    exit /b 1
)

echo [INFO] Python version in use:
python --version
echo.

echo [INFO] Starting Voice Assistant...
echo.

REM Launch the application
python main.py

REM Deactivate on exit
call venv\Scripts\deactivate.bat

echo.
echo ======================================================================
echo   GOODBYE
echo ======================================================================
echo.
