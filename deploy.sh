#!/bin/bash
# ============================================================================
# Ollama Voice Assistant - Deployment Script (Linux/Unix)
# ============================================================================
# This script will:
#   1. Detect compatible Python version (3.9, 3.10, or 3.11)
#   2. Create a virtual environment with the correct Python
#   3. Install all dependencies
#   4. Download Vosk model (if needed)
#   5. Launch the voice assistant
# ============================================================================

echo ""
echo "======================================================================"
echo "  OLLAMA VOICE ASSISTANT - DEPLOYMENT"
echo "======================================================================"
echo ""

# ============================================================================
# Step 0: Detect Compatible Python Version
# ============================================================================

echo "[STEP 0/4] Detecting compatible Python version..."
echo ""

# Initialize Python command variable
PYTHON_CMD=""
PYTHON_VERSION=""

# Function to check Python version compatibility
check_python_version() {
    local cmd=$1
    if ! command -v "$cmd" &> /dev/null; then
        return 1
    fi

    local version=$($cmd --version 2>&1 | grep -oP 'Python \K[0-9]+\.[0-9]+\.[0-9]+' || echo "")
    if [ -z "$version" ]; then
        return 1
    fi

    echo "$version"
    return 0
}

# Function to validate version is compatible (3.9, 3.10, or 3.11)
is_compatible_version() {
    local version=$1
    local major=$(echo "$version" | cut -d. -f1)
    local minor=$(echo "$version" | cut -d. -f2)

    if [ "$major" = "3" ] && ([ "$minor" = "9" ] || [ "$minor" = "10" ] || [ "$minor" = "11" ]); then
        return 0
    fi
    return 1
}

# Try Python 3.11 first (recommended)
for cmd in python3.11 python3.10 python3.9 python3 python; do
    version=$(check_python_version "$cmd")
    if [ $? -eq 0 ]; then
        echo "[INFO] Found $cmd with version $version"
        if is_compatible_version "$version"; then
            PYTHON_CMD="$cmd"
            PYTHON_VERSION="$version"
            echo "[SUCCESS] Using Python $PYTHON_VERSION"
            echo "[INFO] Python command: $PYTHON_CMD"
            echo ""
            break
        fi
    fi
done

# If no compatible version found, show error
if [ -z "$PYTHON_CMD" ]; then
    echo "[ERROR] No compatible Python version found!"
    echo ""
    echo "Required versions: Python 3.9, 3.10, or 3.11"
    echo ""
    echo "Please install Python 3.11 (recommended):"
    echo "  Ubuntu/Debian: sudo apt install python3.11 python3.11-venv"
    echo "  Fedora/RHEL:   sudo dnf install python3.11"
    echo "  Arch:          sudo pacman -S python"
    echo "  macOS:         brew install python@3.11"
    echo ""
    exit 1
fi

# Check if version is compatible, warn if not
if ! is_compatible_version "$PYTHON_VERSION"; then
    major=$(echo "$PYTHON_VERSION" | cut -d. -f1)
    minor=$(echo "$PYTHON_VERSION" | cut -d. -f2)

    echo "======================================================================"
    echo "  WARNING: INCOMPATIBLE PYTHON VERSION DETECTED"
    echo "======================================================================"
    echo ""
    echo "Your Python version: $PYTHON_VERSION"
    echo "Required versions:   3.9, 3.10, or 3.11"
    echo ""

    if [ "$major.$minor" = "3.13" ]; then
        echo "Python 3.13 is TOO NEW - packages like NumPy and Vosk don't have"
        echo "prebuilt wheels yet, causing installation failures."
    elif [ "$major.$minor" = "3.12" ]; then
        echo "Python 3.12 has LIMITED support - some packages may fail to install."
    elif [ "$major" = "3" ] && [ "$minor" -lt 9 ]; then
        echo "Python 3.8 or older is TOO OLD - many packages have dropped support."
    else
        echo "This Python version has not been tested with this project."
    fi

    echo ""
    echo "======================================================================"
    echo "  RECOMMENDED ACTION"
    echo "======================================================================"
    echo ""
    echo "1. Install Python 3.11 (recommended):"
    echo "   Ubuntu/Debian: sudo apt install python3.11 python3.11-venv"
    echo "   Fedora/RHEL:   sudo dnf install python3.11"
    echo "   Arch:          sudo pacman -S python"
    echo "   macOS:         brew install python@3.11"
    echo ""
    echo "2. Then run this script again"
    echo ""
    echo "======================================================================"
    echo ""

    read -p "Do you want to try anyway? (not recommended) [y/N]: " CONTINUE
    if [ "$CONTINUE" != "y" ] && [ "$CONTINUE" != "Y" ]; then
        echo ""
        echo "[INFO] Deployment cancelled. Please install compatible Python version."
        exit 1
    fi

    echo ""
    echo "[WARNING] Proceeding with Python $PYTHON_VERSION..."
    echo "[WARNING] Installation may fail due to incompatible packages!"
    echo ""
fi

# ============================================================================
# Step 1: Create Virtual Environment
# ============================================================================

echo "[STEP 1/4] Creating virtual environment..."
echo ""

if [ -d "venv" ]; then
    echo "[INFO] Virtual environment already exists"
    echo "[WARNING] If you had Python version issues, delete 'venv' folder first"
    echo ""
else
    echo "[INFO] Creating new virtual environment with $PYTHON_CMD..."
    $PYTHON_CMD -m venv venv

    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        echo ""
        echo "Try:"
        echo "  1. Delete the venv folder if it exists: rm -rf venv"
        echo "  2. Install python3-venv: sudo apt install python3.11-venv"
        echo "  3. Run this script again"
        echo ""
        exit 1
    fi

    echo "[SUCCESS] Virtual environment created"
    echo ""
fi

# ============================================================================
# Step 2: Activate Virtual Environment
# ============================================================================

echo "[STEP 2/4] Activating virtual environment..."
echo ""

source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment"
    exit 1
fi

echo "[SUCCESS] Virtual environment activated"
echo ""

# Verify Python version in venv
echo "[INFO] Python version in virtual environment:"
python --version
echo ""

# ============================================================================
# Step 3: Install Dependencies
# ============================================================================

echo "[STEP 3/4] Installing dependencies..."
echo ""

echo "[INFO] Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip setuptools wheel
echo ""

echo "[INFO] Installing requirements from requirements.txt..."
echo "[INFO] This may take several minutes..."
echo ""
pip install -r requirements.txt
PIP_EXIT_CODE=$?

if [ $PIP_EXIT_CODE -ne 0 ]; then
    echo ""
    echo "======================================================================"
    echo "  INSTALLATION FAILED"
    echo "======================================================================"
    echo ""
    echo "[ERROR] Failed to install dependencies"
    echo ""
    echo "Common issues and solutions:"
    echo ""
    echo "1. PYAUDIO INSTALLATION FAILURE:"
    echo "   - Requires PortAudio development headers"
    echo "   - Ubuntu/Debian: sudo apt install portaudio19-dev python3-pyaudio"
    echo "   - Fedora/RHEL:   sudo dnf install portaudio-devel"
    echo "   - macOS:         brew install portaudio"
    echo ""
    echo "2. PYBLUEZ2 INSTALLATION FAILURE:"
    echo "   - Requires Bluetooth development libraries"
    echo "   - Ubuntu/Debian: sudo apt install libbluetooth-dev"
    echo "   - Fedora/RHEL:   sudo dnf install bluez-libs-devel"
    echo "   - Optional - only needed for Bluetooth"
    echo ""
    echo "3. NUMPY/SCIPY COMPILATION ERRORS:"
    echo "   - You're using Python 3.13 which lacks prebuilt wheels"
    echo "   - Solution: Install Python 3.11 and delete venv folder"
    echo ""
    echo "4. MISSING BUILD TOOLS:"
    echo "   - Ubuntu/Debian: sudo apt install build-essential python3-dev"
    echo "   - Fedora/RHEL:   sudo dnf install gcc gcc-c++ python3-devel"
    echo ""
    echo "======================================================================"
    echo ""
    exit 1
fi

echo "[SUCCESS] All dependencies installed"
echo ""

# ============================================================================
# Step 4: Setup Vosk Model
# ============================================================================

echo "[STEP 4/4] Setting up Vosk model..."
echo ""

if [ -d "models/vosk-model-small-en-us-0.15" ]; then
    echo "[INFO] Vosk model already exists"
    echo ""
else
    echo "[INFO] Downloading Vosk model (this may take a few minutes)..."
    python setup_model.py
    MODEL_EXIT_CODE=$?

    if [ $MODEL_EXIT_CODE -ne 0 ]; then
        echo "[ERROR] Failed to download Vosk model"
        echo ""
        echo "[TIP] You can manually download from alphacephei.com/vosk/models"
        echo "      Extract to models/vosk-model-small-en-us-0.15"
        echo ""
        exit 1
    fi

    echo "[SUCCESS] Vosk model downloaded"
    echo ""
fi

# ============================================================================
# Launch Application
# ============================================================================

echo "======================================================================"
echo "  DEPLOYMENT COMPLETE"
echo "======================================================================"
echo ""
echo "[SUCCESS] All setup steps completed successfully!"
echo ""
echo "Python Version: $PYTHON_VERSION"
echo "Virtual Environment: venv/"
echo ""
echo "Starting Voice Assistant..."
echo ""
echo "======================================================================"
echo ""

# Launch the main application
python main.py

# ============================================================================
# Cleanup and Exit
# ============================================================================

echo ""
echo "======================================================================"
echo "  APPLICATION CLOSED"
echo "======================================================================"
echo ""

# Deactivate virtual environment
deactivate

echo ""
echo "Thank you for using Ollama Voice Assistant!"
echo ""
