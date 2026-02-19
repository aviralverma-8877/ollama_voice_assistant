# Deployment Guide

This guide explains how to deploy and run the Ollama Voice Assistant using the automated deployment scripts.

## 📦 Deployment Scripts

Two batch scripts are provided for easy deployment on Windows:

### 1. `deploy.bat` - Initial Setup

Use this script for the **first-time setup**. It automates the entire deployment process.

**What it does:**
1. ✅ Checks if Python is installed
2. ✅ Creates a virtual environment (`venv/`)
3. ✅ Activates the virtual environment
4. ✅ Upgrades pip to the latest version
5. ✅ Installs all dependencies from `requirements.txt`
6. ✅ Downloads the Vosk speech recognition model
7. ✅ Launches the voice assistant

**How to use:**
```bash
# Double-click the file in Windows Explorer
# OR run from command prompt:
deploy.bat
```

### 2. `run.bat` - Quick Launch

Use this script for **subsequent launches** after initial setup.

**What it does:**
1. ✅ Checks if virtual environment exists
2. ✅ Activates the virtual environment
3. ✅ Launches the voice assistant
4. ✅ Deactivates virtual environment on exit

**How to use:**
```bash
# Double-click the file in Windows Explorer
# OR run from command prompt:
run.bat
```

---

## 🎯 Usage Workflow

### First Time Setup:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aviralverma-8877/ollama_voice_assistant.git
   cd ollama_voice_assistant
   ```

2. **Run deployment:**
   ```bash
   deploy.bat
   ```

3. **Wait for setup to complete:**
   - Virtual environment creation: ~30 seconds
   - Dependency installation: ~2-5 minutes
   - Vosk model download: ~1-2 minutes

4. **Choose your mode:**
   - [1] CLI Mode - Terminal with wake word
   - [2] Web Mode - Browser interface

### Subsequent Uses:

1. **Quick launch:**
   ```bash
   run.bat
   ```

2. **Choose your mode and start using!**

---

## 🔧 What Gets Installed

The deployment script installs these components:

### Python Packages:
- **vosk** - Offline speech recognition
- **sounddevice** - Audio I/O
- **numpy** - Numerical processing
- **pyttsx3** - Text-to-speech
- **pybluez2** - Bluetooth support
- **PyAudio** - Audio handling
- **requests** - HTTP client for Ollama
- **Flask** - Web server
- **flask-cors** - CORS support
- **scipy** - Signal processing

### Vosk Model:
- **vosk-model-small-en-us-0.15** (~40MB)
- Downloaded to: `models/vosk-model-small-en-us-0.15/`

---

## 📁 Directory Structure After Deployment

```
ollama-voise-assistant/
├── venv/                    # Virtual environment (created by deploy.bat)
│   ├── Scripts/
│   ├── Lib/
│   └── ...
├── models/                  # Vosk models (downloaded by deploy.bat)
│   └── vosk-model-small-en-us-0.15/
├── deploy.bat              # Initial deployment script
├── run.bat                 # Quick launch script
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
└── ...
```

---

## ⚠️ Troubleshooting

### Problem: "Python is not installed or not in PATH"

**Solution:**
1. Install Python 3.8+ from https://www.python.org/
2. During installation, check "Add Python to PATH"
3. Restart command prompt and try again

### Problem: "Failed to create virtual environment"

**Solution:**
```bash
# Manually create virtual environment:
python -m venv venv

# Then run deploy.bat again
deploy.bat
```

### Problem: "Failed to install dependencies"

**Common issues:**

#### PyAudio Installation Fails:
```bash
# Download PyAudio wheel from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Install manually:
pip install PyAudio-0.2.14-cp39-cp39-win_amd64.whl
```

#### pybluez2 Installation Fails:
```bash
# May require Microsoft Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/downloads/
# Select "Build Tools for Visual Studio 2022"
```

### Problem: "Failed to download Vosk model"

**Solution:**
```bash
# Manually download model:
# 1. Go to: https://alphacephei.com/vosk/models
# 2. Download: vosk-model-small-en-us-0.15.zip
# 3. Extract to: models/vosk-model-small-en-us-0.15/
```

### Problem: Virtual environment activation fails

**Solution:**
```bash
# Set execution policy (run PowerShell as Administrator):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try deploy.bat again
```

### Problem: "Virtual environment not found" when running run.bat

**Solution:**
```bash
# You need to run deploy.bat first:
deploy.bat

# This creates the virtual environment and installs everything
```

---

## 🔄 Updating Dependencies

If `requirements.txt` is updated, reinstall dependencies:

```bash
# Activate virtual environment
venv\Scripts\activate.bat

# Update dependencies
pip install -r requirements.txt --upgrade

# Deactivate
deactivate
```

Or simply delete the `venv/` folder and run `deploy.bat` again.

---

## 🧹 Cleaning Up

### Remove Virtual Environment:
```bash
# Delete the venv folder
rmdir /s /q venv
```

### Remove Downloaded Models:
```bash
# Delete the models folder
rmdir /s /q models
```

### Complete Clean Reinstall:
```bash
# Remove everything
rmdir /s /q venv
rmdir /s /q models

# Run deployment again
deploy.bat
```

---

## 🌐 Network Deployment

To deploy on a server for web mode access:

1. **Run deployment:**
   ```bash
   deploy.bat
   ```

2. **Select Web Mode:**
   ```
   [2] Web Mode
   ```

3. **Configure for network access:**
   ```
   Host: 0.0.0.0
   Port: 5000
   ```

4. **Access from other devices:**
   ```
   http://YOUR_SERVER_IP:5000
   ```

---

## 🔒 Security Notes

- Virtual environment keeps dependencies isolated
- No system-wide package installations
- Easy to delete and recreate
- All data stays local (no cloud services)

---

## 💡 Tips

1. **Create Desktop Shortcut:**
   - Right-click `run.bat`
   - Send to > Desktop (create shortcut)
   - Double-click to launch anytime

2. **Add to Startup:**
   - Press `Win + R`
   - Type: `shell:startup`
   - Copy `run.bat` shortcut to this folder
   - Voice assistant starts with Windows

3. **Check Logs:**
   - If something fails, check console output
   - Error messages indicate what went wrong

4. **Reinstall if Issues:**
   - Delete `venv/` folder
   - Run `deploy.bat` again
   - Fresh installation often fixes issues

---

## 📊 System Requirements

- **OS:** Windows 10/11
- **Python:** 3.8 or higher
- **RAM:** 4GB minimum, 8GB recommended
- **Disk Space:** ~500MB for all dependencies and models
- **Internet:** Required for initial download only

---

## 🎉 Summary

**First time:**
```bash
deploy.bat  # One command does everything!
```

**Every other time:**
```bash
run.bat     # Quick launch
```

That's it! The deployment scripts handle all the complexity for you.

---

## 📝 What Happens Behind the Scenes

### deploy.bat execution flow:

```
1. Check Python installation
   ↓
2. Create virtual environment (venv/)
   ↓
3. Activate virtual environment
   ↓
4. Upgrade pip
   ↓
5. Install requirements.txt
   ↓
6. Run setup_model.py (download Vosk)
   ↓
7. Launch main.py
   ↓
8. User selects mode and uses assistant
   ↓
9. Cleanup on exit
```

### run.bat execution flow:

```
1. Check if venv/ exists
   ↓
2. Activate virtual environment
   ↓
3. Launch main.py
   ↓
4. User selects mode and uses assistant
   ↓
5. Cleanup on exit
```

Simple, automated, and reliable! 🚀
