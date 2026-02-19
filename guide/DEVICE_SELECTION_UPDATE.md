# Device Selection Feature - Update Summary

## ✨ New Feature Added

The voice assistant now includes **interactive audio device selection** when starting the program!

## 🎯 What's New

### User Prompt on Startup

When running `python main.py`, users now see:

```
======================================================================
🎧 Audio Device Setup
======================================================================

Do you want to select audio devices (microphone/speaker)?
  [1] Yes - Let me choose devices
  [2] No  - Use default devices

Your choice [1/2]:
```

### Interactive Device Selection

If the user chooses **[1]**, they can select from all available devices:

- **Input devices** - All microphones (built-in, USB, Bluetooth, etc.)
- **Output devices** - All speakers (built-in, headphones, Bluetooth, etc.)

Each device is numbered for easy selection, with option **[0]** for system default.

## 📝 Changes Made

### Files Modified

1. **`src/audio_manager.py`**
   - ✅ Added `interactive_setup` parameter to `__init__`
   - ✅ Added `_interactive_device_selection()` method
   - ✅ Smart device filtering (input-only vs output-only)
   - ✅ User-friendly device selection interface
   - ✅ Input validation and error handling

2. **`src/voice_assistant.py`**
   - ✅ Added `interactive_audio_setup` parameter to `__init__`
   - ✅ Passes parameter to AudioManager
   - ✅ Maintains backward compatibility

3. **`main.py`**
   - ✅ Added startup prompt for device selection
   - ✅ Respects `PROMPT_DEVICE_SELECTION` config
   - ✅ Handles user choice (1 or 2)
   - ✅ Ctrl+C handling for graceful exit

4. **`src/config.py`**
   - ✅ Added `PROMPT_DEVICE_SELECTION = True` option
   - ✅ Documented new configuration option

### Files Created

1. **`test/test_device_selection.py`**
   - ✅ Standalone test for device selection
   - ✅ Tests the selection interface
   - ✅ Plays test beep on selected device

2. **`DEVICE_SELECTION_GUIDE.md`**
   - ✅ Complete usage guide
   - ✅ Configuration examples
   - ✅ Troubleshooting tips
   - ✅ Common scenarios

3. **`DEVICE_SELECTION_UPDATE.md`** (this file)
   - ✅ Summary of changes
   - ✅ Usage examples
   - ✅ Migration notes

### Documentation Updated

1. **`README.md`**
   - ✅ Updated "How to Use" section
   - ✅ Updated configuration examples
   - ✅ Added device selection section
   - ✅ Updated model name to gemma3:4b

## 🚀 Usage

### Start with Device Selection Prompt (Default)

```bash
python main.py

# Choose option 1 or 2
```

### Test Device Selection

```bash
python -m test.test_device_selection
```

### Disable Device Selection Prompt

Edit `src/config.py`:
```python
PROMPT_DEVICE_SELECTION = False  # No prompt, use defaults
```

### Programmatic Usage

```python
from src.voice_assistant import VoiceAssistant

# Force interactive selection
assistant = VoiceAssistant(interactive_audio_setup=True)

# Force default devices
assistant = VoiceAssistant(interactive_audio_setup=False)
```

## ✅ Features

### Smart Device Detection
- ✅ Filters devices by capability (input vs output)
- ✅ Shows channel information
- ✅ Displays clear device names
- ✅ Numbered selection (1, 2, 3...)

### User Experience
- ✅ Clear prompts and instructions
- ✅ Input validation
- ✅ Option for default devices (0)
- ✅ Graceful error handling
- ✅ Ctrl+C support (exit cleanly)

### Configuration
- ✅ Config option: `PROMPT_DEVICE_SELECTION`
- ✅ Name-based selection: `BLUETOOTH_DEVICE_NAME` (existing)
- ✅ Programmatic control: `interactive_audio_setup` parameter

### Testing
- ✅ Dedicated test script
- ✅ Test beep functionality
- ✅ Device validation

## 📖 Example Workflows

### Example 1: First-Time User

```bash
$ python main.py

🎧 Audio Device Setup
Do you want to select audio devices?
  [1] Yes - Let me choose devices
  [2] No  - Use default devices

Your choice [1/2]: 2

# Uses system defaults - easiest option!
```

### Example 2: Bluetooth Speaker User

```bash
$ python main.py

Your choice [1/2]: 1

📥 Available INPUT devices:
  [1] Built-in Microphone
  [2] Webcam Microphone

Select INPUT device [1-2] or 0 for default: 1

📤 Available OUTPUT devices:
  [1] Built-in Speakers
  [2] Bluetooth Speaker (JBL Flip)

Select OUTPUT device [1-2] or 0 for default: 2

✓ Selected: Bluetooth Speaker
```

### Example 3: USB Headset User

```bash
$ python main.py

Your choice [1/2]: 1

Select INPUT device: 4   # USB Headset Microphone
Select OUTPUT device: 4  # USB Headset Audio

# Both input/output through headset
```

## 🔧 Configuration Options

### Option 1: Always Prompt (Default)

`src/config.py`:
```python
PROMPT_DEVICE_SELECTION = True  # Ask user on startup
```

### Option 2: Never Prompt

`src/config.py`:
```python
PROMPT_DEVICE_SELECTION = False  # Use defaults automatically
```

### Option 3: Auto-Select by Name

`src/config.py`:
```python
BLUETOOTH_DEVICE_NAME = "JBL Flip 5"  # Find device by name
```

## 🎯 Benefits

1. **Flexibility** - Choose any connected audio device
2. **Ease of Use** - Simple numbered menu
3. **Bluetooth Support** - Easy Bluetooth speaker/mic selection
4. **Multiple Setups** - Switch between different device configurations
5. **Default Option** - Quick start with defaults (option 2)
6. **Configuration** - Can disable prompt if not needed

## 🔄 Backward Compatibility

All existing functionality preserved:

- ✅ Default devices still work (no selection needed)
- ✅ `BLUETOOTH_DEVICE_NAME` config still works
- ✅ Existing tests still pass
- ✅ No breaking changes to API

## 📚 Documentation

New and updated documentation:

- ✅ [DEVICE_SELECTION_GUIDE.md](DEVICE_SELECTION_GUIDE.md) - Complete guide
- ✅ [README.md](README.md) - Updated usage instructions
- ✅ [src/config.py](src/config.py) - New config option documented

## 🧪 Testing

Test the feature:

```bash
# Test device selection interface
python -m test.test_device_selection

# Test with full assistant (choose option 1)
python main.py
```

## 🎉 Summary

The audio device selection feature is now live! Users can:

1. **Select devices interactively** when starting the assistant
2. **Use default devices** with a single keypress (option 2)
3. **Disable the prompt** via configuration
4. **Test the feature** with a dedicated test script

The feature is:
- ✅ User-friendly
- ✅ Fully configurable
- ✅ Well-documented
- ✅ Backward compatible
- ✅ Thoroughly tested

Happy voice assisting! 🎤🔊
