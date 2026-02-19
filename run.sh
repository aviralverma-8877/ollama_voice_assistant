#!/bin/bash
# ============================================================================
# Ollama Voice Assistant - Quick Launch Script (Linux/Unix)
# ============================================================================
# Use this script for quick launches after initial deployment
# If this is your first time, run deploy.sh instead
# ============================================================================

echo ""
echo "======================================================================"
echo "  OLLAMA VOICE ASSISTANT - QUICK LAUNCH"
echo "======================================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[ERROR] Virtual environment not found!"
    echo ""
    echo "Please run deploy.sh first to set up the environment."
    echo ""
    exit 1
fi

echo "[INFO] Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment"
    echo ""
    echo "Try running deploy.sh again to fix the environment."
    echo ""
    exit 1
fi

echo "[INFO] Python version in use:"
python --version
echo ""

echo "[INFO] Starting Voice Assistant..."
echo ""

# Launch the application
python main.py

# Deactivate on exit
deactivate

echo ""
echo "======================================================================"
echo "  GOODBYE"
echo "======================================================================"
echo ""
