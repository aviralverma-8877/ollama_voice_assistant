# Audio Device Selection Guide

This guide explains how to use the interactive audio device selection feature.

## Overview

The voice assistant now allows you to select your preferred microphone (input) and speaker (output) devices when starting the program. This is useful when you have multiple audio devices connected (e.g., webcam microphone, headset, Bluetooth speaker, etc.).

## How It Works

### Starting the Assistant

When you run `python main.py`, you'll see:

```
======================================================================
🎧 Audio Device Setup
======================================================================

Do you want to select audio devices (microphone/speaker)?
  [1] Yes - Let me choose devices
  [2] No  - Use default devices

Your choice [1/2]:
```

### Option 1: Manual Selection

If you choose **[1] Yes**, you'll see all available devices:

```
======================================================================
AUDIO DEVICE SELECTION
======================================================================

📥 Available INPUT devices (Microphones):
  [1] Microsoft Sound Mapper - Input
  [2] Microphone Array on SoundWire Device
  [3] Webcam Microphone
  [4] Headset Microphone

📤 Available OUTPUT devices (Speakers):
  [1] Microsoft Sound Mapper - Output
  [2] Speakers (Cirrus Logic XU)
  [3] Headphones
  [4] Bluetooth Speaker

----------------------------------------------------------------------

Select INPUT device [1-4] or 0 for default: 3

✓ Selected: Webcam Microphone

----------------------------------------------------------------------

Select OUTPUT device [1-4] or 0 for default: 4

✓ Selected: Bluetooth Speaker

======================================================================
SELECTED DEVICES:
======================================================================
  Input:  Webcam Microphone
  Output: Bluetooth Speaker
======================================================================
```

### Option 2: Default Devices

If you choose **[2] No**, the assistant will use your system's default audio devices (usually the correct choice).

## Configuration

### Disable the Prompt

If you don't want to be prompted every time, edit [src/config.py](src/config.py):

```python
PROMPT_DEVICE_SELECTION = False  # Skip device selection prompt
```

The assistant will then use default devices automatically.

### Pre-select Devices by Name

You can also configure a specific device by name in [src/config.py](src/config.py):

```python
BLUETOOTH_DEVICE_NAME = "JBL Flip 5"  # Auto-select by name
```

This will automatically find and use any device with "JBL Flip 5" in its name.

## Testing Device Selection

Test the device selection feature without starting the full assistant:

```bash
python -m test.test_device_selection
```

This will:
1. Show all available devices
2. Let you select input/output
3. Play a test beep on the selected output device

## Common Scenarios

### Scenario 1: Using Bluetooth Speaker

```
Your choice [1/2]: 1

Select INPUT device: 0  (use default microphone)
Select OUTPUT device: 4  (select Bluetooth speaker)
```

**Result**: Uses built-in microphone, outputs to Bluetooth speaker

### Scenario 2: Using Headset

```
Your choice [1/2]: 1

Select INPUT device: 3  (select headset microphone)
Select OUTPUT device: 3  (select headset speakers)
```

**Result**: Both input and output through headset

### Scenario 3: First Time User

```
Your choice [1/2]: 2  (use defaults)
```

**Result**: Uses system default devices (recommended)

## Troubleshooting

### Issue: Device Not Listed

**Solution**: Make sure the device is:
- Properly connected to your computer
- Powered on (for Bluetooth devices)
- Paired (for Bluetooth devices)
- Not in use by another application

### Issue: Selected Device Doesn't Work

**Possible causes**:
1. Device disconnected after selection
2. Device is muted
3. Wrong device permissions

**Solution**:
- Try using default devices (option 2)
- Check Windows audio settings
- Restart the application

### Issue: Want to Change Devices

**Solution**:
- Restart the application: `python main.py`
- Select different devices when prompted

### Issue: Prompt Appears Every Time

**Solution**: To skip the prompt, edit [src/config.py](src/config.py):
```python
PROMPT_DEVICE_SELECTION = False
```

## Command-Line Usage

For advanced users, you can also create a custom launcher script:

```python
# custom_launcher.py
from src.voice_assistant import VoiceAssistant

# Always use interactive selection
assistant = VoiceAssistant(interactive_audio_setup=True)
assistant.run()
```

Or always skip selection:

```python
# auto_launcher.py
from src.voice_assistant import VoiceAssistant

# Never prompt for device selection
assistant = VoiceAssistant(interactive_audio_setup=False)
assistant.run()
```

## Features

### Smart Device Detection
- Automatically filters input-only and output-only devices
- Shows device capabilities (channels, etc.)
- Handles device disconnection gracefully

### User-Friendly Interface
- Clear numbering system (1, 2, 3...)
- Option 0 for system default
- Input validation (rejects invalid choices)
- Ctrl+C handling (exits gracefully)

### Flexible Configuration
- Config file option: `PROMPT_DEVICE_SELECTION`
- Name-based selection: `BLUETOOTH_DEVICE_NAME`
- Programmatic control: `interactive_audio_setup` parameter

## Device Types Supported

- **Built-in microphones** (laptop, webcam)
- **USB microphones** (external mics)
- **Bluetooth microphones** (wireless headsets)
- **Built-in speakers** (laptop speakers)
- **Wired speakers/headphones** (3.5mm jack, USB)
- **Bluetooth speakers** (wireless speakers, earbuds)
- **HDMI audio** (monitor speakers)
- **Virtual audio devices** (OBS, VoiceMeeter, etc.)

## Best Practices

1. **First-time users**: Choose option [2] (default devices)
2. **Bluetooth users**: Choose option [1] and select your Bluetooth device
3. **Multiple setups**: Use device selection each time
4. **Single setup**: Disable prompt in config and use defaults

## Examples

### Example 1: Laptop with Bluetooth Speaker

```bash
$ python main.py

Your choice [1/2]: 1

# Select laptop microphone for input
Select INPUT device: 1

# Select Bluetooth speaker for output
Select OUTPUT device: 5

# Now the assistant listens through laptop mic
# and speaks through Bluetooth speaker
```

### Example 2: USB Headset

```bash
$ python main.py

Your choice [1/2]: 1

# Select USB headset for both
Select INPUT device: 6   # USB Headset Mic
Select OUTPUT device: 6  # USB Headset Audio

# Complete audio setup through USB headset
```

### Example 3: Default Setup

```bash
$ python main.py

Your choice [1/2]: 2

# Uses system defaults - quickest option!
```

## Summary

The audio device selection feature gives you complete control over which microphone and speaker the voice assistant uses. It's:

- ✅ **Easy to use** - Simple numbered menu
- ✅ **Flexible** - Can be enabled/disabled
- ✅ **Smart** - Filters appropriate devices
- ✅ **Safe** - Validates all inputs
- ✅ **Optional** - Default devices work great

For most users, the default devices (option 2) work perfectly. Use manual selection when you have multiple audio devices or specific hardware requirements.
