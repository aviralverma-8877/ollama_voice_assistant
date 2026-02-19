# Python Version Compatibility Guide

This guide helps you choose the right Python version and troubleshoot installation issues.

## 🐍 Recommended Python Versions

### ✅ Highly Recommended (Best Compatibility)

| Version | Status | Notes |
|---------|--------|-------|
| **Python 3.9** | ✅ **Best Choice** | Most stable, excellent package support |
| **Python 3.10** | ✅ **Recommended** | Great compatibility, good performance |
| **Python 3.11** | ✅ **Recommended** | Faster performance, good support |

### ⚠️ May Work But Not Ideal

| Version | Status | Notes |
|---------|--------|-------|
| Python 3.12 | ⚠️ Limited | Some packages may lack prebuilt wheels |
| Python 3.8 | ⚠️ Aging | Works but support is waning |

### ❌ Not Supported

| Version | Status | Notes |
|---------|--------|-------|
| Python 3.7 or older | ❌ Not Supported | End of life, incompatible packages |
| Python 2.x | ❌ Not Supported | Completely deprecated |

---

## 🔧 Why NumPy Fails to Install

NumPy installation failures are common and usually due to:

### 1. No Prebuilt Wheel for Your Python Version

**Problem:**
```
ERROR: Could not find a version that satisfies the requirement numpy
```

**Solution:**
```bash
# Use Python 3.9, 3.10, or 3.11
# These have the best wheel support
```

### 2. Missing C Compiler

**Problem:**
```
error: Microsoft Visual C++ 14.0 or greater is required
```

**Solution:**

**Option A (Recommended):** Use prebuilt wheels
```bash
# Use Python 3.9-3.11 which have prebuilt wheels
# No compiler needed!
```

**Option B:** Install compiler
1. Download "Build Tools for Visual Studio 2022"
2. Install "Desktop development with C++"
3. Try installation again

### 3. Outdated pip/setuptools

**Problem:**
```
error: invalid command 'bdist_wheel'
```

**Solution:**
```bash
# Upgrade pip, setuptools, and wheel
python -m pip install --upgrade pip setuptools wheel

# Then try again
pip install -r requirements.txt
```

---

## 📊 Package Compatibility Matrix

| Package | Python 3.9 | Python 3.10 | Python 3.11 | Python 3.12 |
|---------|------------|-------------|-------------|-------------|
| numpy | ✅ | ✅ | ✅ | ⚠️ |
| scipy | ✅ | ✅ | ✅ | ⚠️ |
| vosk | ✅ | ✅ | ✅ | ⚠️ |
| Flask | ✅ | ✅ | ✅ | ✅ |
| pyttsx3 | ✅ | ✅ | ✅ | ✅ |
| PyAudio | ⚠️ (needs wheel) | ⚠️ (needs wheel) | ⚠️ (needs wheel) | ❌ |

**Legend:**
- ✅ Full support with prebuilt wheels
- ⚠️ May need workarounds or manual installation
- ❌ Not supported or very difficult

---

## 🚀 Installation Best Practices

### 1. Check Your Python Version

```bash
python --version
# Should show: Python 3.9.x, 3.10.x, or 3.11.x
```

### 2. Use Virtual Environment (Strongly Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Verify you're in the venv
which python  # Linux/Mac
where python  # Windows
```

### 3. Upgrade pip First

```bash
python -m pip install --upgrade pip setuptools wheel
```

### 4. Install Requirements

```bash
pip install -r requirements.txt
```

---

## 🩹 Troubleshooting Common Issues

### Issue: "numpy installation fails"

**Try these steps in order:**

1. **Check Python version:**
   ```bash
   python --version
   # Use 3.9, 3.10, or 3.11
   ```

2. **Upgrade pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

3. **Install numpy separately first:**
   ```bash
   pip install numpy>=1.24.0
   ```

4. **Then install rest:**
   ```bash
   pip install -r requirements.txt
   ```

### Issue: "PyAudio installation fails"

**Solution:** Download prebuilt wheel

1. **Visit:** https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. **Download** wheel matching your Python version:
   - Python 3.9 64-bit: `PyAudio‑0.2.14‑cp39‑cp39‑win_amd64.whl`
   - Python 3.10 64-bit: `PyAudio‑0.2.14‑cp310‑cp310‑win_amd64.whl`
   - Python 3.11 64-bit: `PyAudio‑0.2.14‑cp311‑cp311‑win_amd64.whl`
3. **Install:**
   ```bash
   pip install PyAudio‑0.2.14‑cp39‑cp39‑win_amd64.whl
   ```

### Issue: "pybluez2 installation fails"

**Solution:** This package may have limited Windows support

**Option A:** Skip Bluetooth support
```bash
# Remove pybluez2 from requirements.txt
# The assistant will still work without it
```

**Option B:** Install Visual C++ Build Tools (if you need Bluetooth)
1. Download Build Tools for Visual Studio
2. Install "Desktop development with C++"
3. Retry installation

---

## 🔄 Switching Python Versions

### If You Need to Change Python Version:

1. **Install the recommended Python version:**
   - Download from: https://www.python.org/downloads/
   - Choose 3.9, 3.10, or 3.11

2. **Delete old virtual environment:**
   ```bash
   rmdir /s /q venv  # Windows
   rm -rf venv       # Linux/Mac
   ```

3. **Create new venv with correct Python:**
   ```bash
   # Use specific Python version
   py -3.9 -m venv venv  # Windows
   python3.9 -m venv venv  # Linux/Mac
   ```

4. **Activate and install:**
   ```bash
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

---

## 📦 System Requirements

### Minimum:
- Python 3.9 or higher
- pip 21.0+
- 4GB RAM
- Windows 10/11, Linux, or macOS

### Recommended:
- **Python 3.9, 3.10, or 3.11**
- pip 23.0+
- 8GB RAM
- SSD storage

---

## 🧪 Testing Your Installation

After installing, verify everything works:

```bash
# Test numpy
python -c "import numpy; print(f'NumPy {numpy.__version__}')"

# Test scipy
python -c "import scipy; print(f'SciPy {scipy.__version__}')"

# Test vosk
python -c "import vosk; print('Vosk OK')"

# Test Flask
python -c "import flask; print(f'Flask {flask.__version__}')"

# Run full test suite
python -m test.test_web_server
```

If all imports succeed, you're good to go!

---

## 💡 Quick Reference

### Best Python Version for This Project:

```
🎯 Python 3.9, 3.10, or 3.11
   (3.9 recommended for maximum stability)
```

### Installation Command:

```bash
# After installing Python 3.9-3.11:
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### If NumPy Still Fails:

```bash
# Try installing numpy first, separately:
pip install numpy>=1.24.0

# Then the rest:
pip install -r requirements.txt
```

---

## 📞 Still Having Issues?

1. **Check Python version:** Must be 3.9, 3.10, or 3.11
2. **Use virtual environment:** Isolates dependencies
3. **Upgrade pip:** `python -m pip install --upgrade pip`
4. **Install Visual Studio Build Tools:** For packages that need compilation
5. **Use prebuilt wheels:** For PyAudio and other binary packages

If problems persist, check the error message for specific package names and search for "[package-name] [Python-version] Windows wheel" to find prebuilt solutions.

---

## ✅ Summary

**For the best experience with this project:**

1. ✅ Use **Python 3.9, 3.10, or 3.11**
2. ✅ Always use a **virtual environment**
3. ✅ Upgrade pip **before** installing requirements
4. ✅ Install packages in order: numpy first, then others
5. ✅ Use **prebuilt wheels** for PyAudio on Windows

Following these guidelines will give you a smooth installation experience! 🚀
