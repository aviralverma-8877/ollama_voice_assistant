# Quick Start Guide

Get your Ollama Voice Assistant running in 3 simple steps!

## Prerequisites
- Python 3.8 or higher
- Ollama running on your server (https://home.iot-connect.in)
- Microphone and speakers (or Bluetooth audio device)

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note for Windows users:** If PyAudio installation fails, download the wheel file:
- Visit: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- Download the appropriate `.whl` file for your Python version
- Install with: `pip install PyAudio‑0.2.11‑cp3XX‑cp3XX‑win_amd64.whl`

## Step 2: Download Vosk Model

Run the automated setup:
```bash
python setup_model.py
```

Or manually:
1. Visit: https://alphacephei.com/vosk/models
2. Download: `vosk-model-small-en-us-0.15.zip` (39 MB)
3. Extract to: `models/vosk-model-small-en-us-0.15/`

## Step 3: Configure (Optional)

Edit [src/config.py](src/config.py) if needed:
- Change Ollama model: `OLLAMA_MODEL = "llama3"`
- Set Bluetooth device: `BLUETOOTH_DEVICE_NAME = "Your Device"`
- Adjust wake word: `WAKE_WORD = "hey assistant"`

## Step 4: Test (Optional but Recommended)

Verify everything is working:
```bash
python -m test.test_components
```

Or run a quick demo:
```bash
python -m test.demo_test
```

This will check:
- All dependencies are installed
- Vosk model is available
- Audio devices are detected
- Text-to-speech works
- Ollama is accessible

## Step 5: Run!

```bash
python main.py
```

## Usage

1. **Activate**: Say "hello lamma"
2. **Wait**: Listen for the beep sound
3. **Speak**: Ask your question or give a command
4. **Listen**: Hear the assistant's response
5. **Continue**: Say "hello lamma" again for another query
6. **Exit**: Say "goodbye" to end the session

## Troubleshooting

### No audio input/output
- Check microphone permissions
- Try setting `BLUETOOTH_DEVICE_NAME = None` in config.py

### Can't connect to Ollama
- Verify Ollama is running: `curl https://home.iot-connect.in/api/tags`
- Check the URL in config.py
- Ensure the model is pulled: `ollama pull llama2`

### Wake word not detecting
- Speak clearly and at normal volume
- Try adjusting microphone position
- Check the wake word spelling in config.py

### PyAudio errors on Windows
- Install from wheel file (see Step 1 note above)
- Or try: `pip install pipwin && pipwin install pyaudio`

## Advanced Configuration

### Change TTS Voice
In your Python console:
```python
from text_to_speech import TextToSpeech
tts = TextToSpeech()
tts.list_voices()  # See available voices
```

Then in voice_assistant.py, add after TTS initialization:
```python
self.tts.set_voice(1)  # Change index to your preferred voice
```

### Adjust Speech Rate
In config.py or when initializing:
```python
self.tts = TextToSpeech(rate=180)  # Default: 150 WPM
```

### Use Different Vosk Model
Download a different model from https://alphacephei.com/vosk/models
- Small (39 MB): Fast, good accuracy
- Large (1.8 GB): Best accuracy, slower

Update `VOSK_MODEL_PATH` in config.py

## Need Help?

Check the main [README.md](README.md) for detailed information about each component.
