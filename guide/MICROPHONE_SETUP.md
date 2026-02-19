# Microphone Setup Guide

## The Problem
Your voice assistant isn't recognizing your speech because the microphone volume is too low. The audio is being captured, but at levels too low for Vosk speech recognition to process effectively.

## Current Status
- ✅ Microphone is working (audio is being recorded)
- ✅ Audio is being saved to files successfully
- ❌ Volume is too low (only 5-15% of maximum)
- ❌ Vosk can't recognize speech at these levels

## Solution: Increase Windows Microphone Volume

### Step 1: Open Sound Settings
Choose one of these methods:

**Method 1 - Using Settings:**
1. Press `Windows + I` to open Settings
2. Go to **System** → **Sound**
3. Scroll down to **Input**
4. Click on your microphone device

**Method 2 - Using Control Panel:**
1. Press `Windows + R`
2. Type: `mmsys.cpl` and press Enter
3. Go to the **Recording** tab
4. Double-click on "Microphone Array on SoundWire D"

### Step 2: Adjust Microphone Settings

1. **Set Volume to 100%**
   - Move the volume slider all the way to the right
   - This is the most important step

2. **Enable Microphone Boost** (if available)
   - Look for "Boost" or "Microphone Boost" option
   - Set it to **+20 dB** or **+30 dB**
   - This significantly amplifies weak signals

3. **Disable Noise Suppression** (temporarily for testing)
   - Look for "Noise suppression" or "Noise cancellation"
   - Turn it OFF for now
   - You can re-enable it later once speech recognition is working

4. **Check "Listen to this device"** (optional, for immediate feedback)
   - This lets you hear yourself through speakers
   - Useful for testing microphone levels
   - **Warning:** May cause echo/feedback, use carefully

### Step 3: Test Your Microphone

Run this test to verify the changes:
```bash
python -m test.test_microphone
```

You should see much higher amplitude values now (ideally 10,000-30,000).

### Step 4: Test Speech Recognition

Once microphone volume is increased, test speech recognition:
```bash
python -m test.test_simple_wake_word
```

When prompted, speak **LOUDLY and CLEARLY** into the microphone.

## Troubleshooting

### If you still get low audio levels:

1. **Check if microphone is muted**
   - Look for a mute icon next to the microphone in Settings
   - Unmute it if it's muted

2. **Try a different microphone**
   - Run the main program with device selection:
     ```bash
     python main.py
     ```
   - Choose option 1 to select a different microphone
   - Try each microphone device and see which one works best

3. **Check physical microphone**
   - If using an external microphone, ensure it's plugged in
   - Check if there's a physical mute switch on the device
   - Try moving closer to the microphone

4. **Update audio drivers**
   - Open Device Manager
   - Expand "Sound, video and game controllers"
   - Right-click on your audio device
   - Select "Update driver"

## Expected Results

After increasing microphone volume, you should see:
- Max amplitude: **10,000-30,000** (good)
- Speech recognition: **Text appears** when you speak
- Wake word detection: **Responds to "hello lamma"**

## Quick Command Reference

```bash
# Test microphone levels
python -m test.test_microphone

# Test speech recognition
python -m test.test_simple_wake_word

# Save recording to WAV file
python -m test.test_save_recording

# Run the full assistant
python main.py
```

## Current Device Information

Based on diagnostics:
- **Input Device:** Microphone Array on SoundWire D
- **Output Device:** Speakers (Cirrus Logic XU)
- **Sample Rate:** 16000 Hz (required by Vosk)
- **Channels:** Mono (1 channel)

## Need More Help?

If you've followed all steps and it still doesn't work:

1. Check the saved recording:
   - Play `test_outputs/test_recording.wav`
   - If you can hear your voice clearly, the issue is with Vosk configuration
   - If you can't hear your voice, the issue is with microphone settings

2. Try different wake words:
   - Edit `src/config.py`
   - Change `WAKE_WORD = "hello lamma"` to something easier like `"hello"`

3. Try a larger Vosk model:
   - Download from: https://alphacephei.com/vosk/models
   - Try "vosk-model-en-us-0.22" (larger, more accurate)
   - Update `VOSK_MODEL_PATH` in `src/config.py`
