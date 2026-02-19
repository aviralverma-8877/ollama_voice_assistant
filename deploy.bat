@echo off
REM ============================================================================
REM Ollama Voice Assistant - Deployment Script
REM ============================================================================
REM This script will:
REM   1. Detect compatible Python version (3.9, 3.10, or 3.11)
REM   2. Create a virtual environment with the correct Python
REM   3. Install all dependencies
REM   4. Download Vosk model (if needed)
REM   5. Launch the voice assistant
REM ============================================================================

echo.
echo ======================================================================
echo   OLLAMA VOICE ASSISTANT - DEPLOYMENT
echo ======================================================================
echo.

REM ============================================================================
REM Step 0: Detect Compatible Python Version
REM ============================================================================

echo [STEP 0/4] Detecting compatible Python version...
echo.

REM Initialize Python command variable
set PYTHON_CMD=
set PYTHON_VERSION=

REM Check if Python launcher (py) is available
py --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Python launcher 'py' not found, trying 'python'...
    python --version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python is not installed or not in PATH
        echo.
        echo Please install Python 3.9, 3.10, or 3.11 from:
        echo   python.org/downloads
        echo.
        pause
        exit /b 1
    )
    set PYTHON_CMD=python
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    goto :version_check
)

REM Try Python 3.11 first (recommended)
py -3.11 --version >nul 2>&1
if not errorlevel 1 (
    echo [SUCCESS] Found Python 3.11
    set PYTHON_CMD=py -3.11
    for /f "tokens=2" %%i in ('py -3.11 --version 2^>^&1') do set PYTHON_VERSION=%%i
    goto :version_found
)

REM Try Python 3.10
py -3.10 --version >nul 2>&1
if not errorlevel 1 (
    echo [SUCCESS] Found Python 3.10
    set PYTHON_CMD=py -3.10
    for /f "tokens=2" %%i in ('py -3.10 --version 2^>^&1') do set PYTHON_VERSION=%%i
    goto :version_found
)

REM Try Python 3.9
py -3.9 --version >nul 2>&1
if not errorlevel 1 (
    echo [SUCCESS] Found Python 3.9
    set PYTHON_CMD=py -3.9
    for /f "tokens=2" %%i in ('py -3.9 --version 2^>^&1') do set PYTHON_VERSION=%%i
    goto :version_found
)

REM No compatible version found via py launcher, check default python
echo [WARNING] No compatible Python version found via py launcher
echo [INFO] Checking default 'python' command...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.9, 3.10, or 3.11 from:
    echo   python.org/downloads
    echo.
    pause
    exit /b 1
)

set PYTHON_CMD=python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i

:version_check
REM Check if version is compatible
echo [INFO] Detected Python version: %PYTHON_VERSION%
echo.

REM Extract major and minor version
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

REM Check if version is 3.9, 3.10, or 3.11
if "%MAJOR%.%MINOR%"=="3.9" goto :version_ok
if "%MAJOR%.%MINOR%"=="3.10" goto :version_ok
if "%MAJOR%.%MINOR%"=="3.11" goto :version_ok

REM Version is not compatible
echo ======================================================================
echo   WARNING: INCOMPATIBLE PYTHON VERSION DETECTED
echo ======================================================================
echo.
echo Your Python version: %PYTHON_VERSION%
echo Required versions:   3.9, 3.10, or 3.11
echo.
if "%MAJOR%.%MINOR%"=="3.13" (
    echo Python 3.13 is TOO NEW - packages like NumPy and Vosk don't have
    echo prebuilt wheels yet, causing installation failures.
) else if "%MAJOR%.%MINOR%"=="3.12" (
    echo Python 3.12 has LIMITED support - some packages may fail to install.
) else if "%MAJOR%"=="3" (
    if %MINOR% LSS 9 (
        echo Python 3.8 or older is TOO OLD - many packages have dropped support.
    ) else (
        echo This Python version has not been tested with this project.
    )
) else (
    echo Python 2.x is NOT SUPPORTED.
)
echo.
echo ======================================================================
echo   RECOMMENDED ACTION
echo ======================================================================
echo.
echo 1. Install Python 3.11 (recommended):
echo    python.org/downloads
echo.
echo 2. Then run this script again
echo.
echo If you have Python 3.11 installed, you can specify it:
echo    py -3.11 -m venv venv
echo.
echo ======================================================================
echo.
set /p CONTINUE="Do you want to try anyway? (not recommended) [y/N]: "
if /i not "%CONTINUE%"=="y" (
    echo.
    echo [INFO] Deployment cancelled. Please install compatible Python version.
    pause
    exit /b 1
)
echo.
echo [WARNING] Proceeding with Python %PYTHON_VERSION%...
echo [WARNING] Installation may fail due to incompatible packages!
echo.

:version_ok
:version_found

echo [SUCCESS] Using Python %PYTHON_VERSION%
echo [INFO] Python command: %PYTHON_CMD%
echo.

REM ============================================================================
REM Step 1: Create Virtual Environment
REM ============================================================================

echo [STEP 1/4] Creating virtual environment...
echo.

if exist "venv" (
    echo [INFO] Virtual environment already exists
    echo [WARNING] If you had Python version issues, delete 'venv' folder first
    echo.
) else (
    echo [INFO] Creating new virtual environment with %PYTHON_CMD%...
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        echo.
        echo Try:
        echo   1. Delete the venv folder if it exists
        echo   2. Install Python 3.11 from python.org
        echo   3. Run this script again
        echo.
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

REM Verify Python version in venv
echo [INFO] Python version in virtual environment:
python --version
echo.

REM ============================================================================
REM Step 3: Install Dependencies
REM ============================================================================

echo [STEP 3/4] Installing dependencies...
echo.

echo [INFO] Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel
echo.

echo [INFO] Installing requirements from requirements.txt...
echo [INFO] This may take several minutes...
echo.
pip install -r requirements.txt
set PIP_EXIT_CODE=%ERRORLEVEL%

if not "%PIP_EXIT_CODE%"=="0" (
    echo.
    echo ======================================================================
    echo   INSTALLATION FAILED
    echo ======================================================================
    echo.
    echo [ERROR] Failed to install dependencies
    echo.
    echo Common issues and solutions:
    echo.
    echo 1. NUMPY/SCIPY COMPILATION ERRORS: vswhere.exe missing
    echo    - You're using Python 3.13 which lacks prebuilt wheels
    echo    - Solution: Install Python 3.11 and delete venv folder
    echo    - Download from python.org
    echo.
    echo 2. PYAUDIO INSTALLATION FAILURE:
    echo    - Download wheel from gohlke pythonlibs
    echo    - Install manually with pip install
    echo.
    echo 3. PYBLUEZ2 INSTALLATION FAILURE:
    echo    - Requires Visual C++ Build Tools
    echo    - Optional - only needed for Bluetooth
    echo    - Can be skipped by removing from requirements.txt
    echo.
    echo See guide\PYTHON_COMPATIBILITY.md for detailed troubleshooting
    echo.
    echo ======================================================================
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
    echo [INFO] Downloading Vosk model (this may take a few minutes^)...
    python setup_model.py
    set MODEL_EXIT_CODE=%ERRORLEVEL%

    if not "%MODEL_EXIT_CODE%"=="0" (
        echo [ERROR] Failed to download Vosk model
        echo.
        echo [TIP] You can manually download from alphacephei.com/vosk/models
        echo      Extract to models\vosk-model-small-en-us-0.15
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
echo Python Version: %PYTHON_VERSION%
echo Virtual Environment: venv\
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
