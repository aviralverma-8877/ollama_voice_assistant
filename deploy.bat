@echo off
REM ============================================================================
REM Ollama Voice Assistant - Deployment Script
REM ============================================================================
REM This script will:
REM   1. Create a virtual environment
REM   2. Install all dependencies
REM   3. Download Vosk model (if needed)
REM   4. Launch the voice assistant
REM ============================================================================

echo.
echo ======================================================================
echo   OLLAMA VOICE ASSISTANT - DEPLOYMENT
echo ======================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [INFO] Python detected:
python --version
echo.

REM ============================================================================
REM Step 1: Create Virtual Environment
REM ============================================================================

echo [STEP 1/4] Creating virtual environment...
echo.

if exist "venv" (
    echo [INFO] Virtual environment already exists
    echo.
) else (
    echo [INFO] Creating new virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created
    echo.
)

REM ============================================================================
REM Step 2: Activate Virtual Environment
REM ============================================================================

echo [STEP 2/4] Activating virtual environment...
echo.

call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

echo [SUCCESS] Virtual environment activated
echo.

REM ============================================================================
REM Step 3: Install Dependencies
REM ============================================================================

echo [STEP 3/4] Installing dependencies...
echo.

echo [INFO] Upgrading pip...
python -m pip install --upgrade pip
echo.

echo [INFO] Installing requirements from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    echo.
    echo [TIP] Some packages may require manual installation:
    echo   - PyAudio: Download wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/
    echo   - pybluez2: May require Microsoft Visual C++ Build Tools
    echo.
    pause
    exit /b 1
)

echo [SUCCESS] All dependencies installed
echo.

REM ============================================================================
REM Step 4: Setup Vosk Model
REM ============================================================================

echo [STEP 4/4] Setting up Vosk model...
echo.

if exist "models\vosk-model-small-en-us-0.15" (
    echo [INFO] Vosk model already exists
    echo.
) else (
    echo [INFO] Downloading Vosk model (this may take a few minutes)...
    python setup_model.py
    if errorlevel 1 (
        echo [ERROR] Failed to download Vosk model
        echo.
        echo [TIP] You can manually download from:
        echo   https://alphacephei.com/vosk/models
        echo   Extract to: models\vosk-model-small-en-us-0.15
        echo.
        pause
        exit /b 1
    )
    echo [SUCCESS] Vosk model downloaded
    echo.
)

REM ============================================================================
REM Launch Application
REM ============================================================================

echo ======================================================================
echo   DEPLOYMENT COMPLETE
echo ======================================================================
echo.
echo [SUCCESS] All setup steps completed successfully!
echo.
echo Starting Voice Assistant...
echo.
echo ======================================================================
echo.

REM Launch the main application
python main.py

REM ============================================================================
REM Cleanup and Exit
REM ============================================================================

echo.
echo ======================================================================
echo   APPLICATION CLOSED
echo ======================================================================
echo.

REM Keep window open if there was an error
if errorlevel 1 (
    echo [ERROR] Application exited with an error
    pause
)

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat

echo.
echo Thank you for using Ollama Voice Assistant!
echo.
pause
