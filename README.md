# Ollama Voice Assistant

A fully-featured voice-activated assistant powered by Ollama for local LLM inference.

## ✨ Features

- 🎯 **Wake Word Detection**: Activate with "hello lamma"
- 🎤 **Speech-to-Text**: Powered by Vosk (fully offline)
- 🔊 **Text-to-Speech**: Using pyttsx3 (fully offline)
- 🤖 **Ollama Integration**: Maintains conversation context
- 🔵 **Bluetooth Support**: Works with Bluetooth speakers/microphones
- 💬 **Session Management**: Remembers conversation history
- 🔔 **Audio Feedback**: Beep notification when activated

## 🚀 Quick Start

See [QUICKSTART.md](QUICKSTART.md) for a step-by-step guide!

**TL;DR:**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download Vosk model
python setup_model.py

# 3. Run the assistant
python main.py
```

## 🧪 Testing

Before using voice input, test the system:

```bash
# Verify all components
python -m test.test_components

# Test Ollama integration and generate response audio
python -m test.demo_test

# Run simple pipeline test
python -m test.test_simple

# Check output files in test_outputs/ directory
```

See [TEST_GUIDE.md](TEST_GUIDE.md) for detailed testing instructions.

## 📋 Requirements

- **Python 3.8+**
- **Ollama** running on your server (configured URL: `https://home.iot-connect.in`)
- **Microphone** for voice input
- **Speakers** for audio output (Bluetooth supported)

## 🎮 How to Use

1. **Start**: Run `python main.py`
2. **Select Audio Devices**: Choose your microphone and speaker (optional)
   - Option 1: Manually select from available devices
   - Option 2: Use default devices (recommended for most users)
3. **Activate**: Say "hello lamma"
4. **Listen**: Wait for the beep sound
5. **Speak**: Ask your question
6. **Hear**: Listen to the response
7. **Continue**: Say "hello lamma" for next query
8. **Exit**: Say "goodbye" to end

## 📁 Project Structure

```
ollama-voise-assistant/
├── main.py                  # Main entry point - run this to start
├── setup_model.py           # Vosk model downloader
├── requirements.txt         # Python dependencies
├── src/                     # Source code
│   ├── __init__.py
│   ├── config.py            # Configuration settings
│   ├── voice_assistant.py   # Main assistant logic
│   ├── audio_manager.py     # Audio I/O and Bluetooth
│   ├── wake_word_detector.py# Wake word detection
│   ├── speech_to_text.py    # STT using Vosk
│   ├── text_to_speech.py    # TTS using pyttsx3
│   └── ollama_client.py     # Ollama API integration
├── test/                    # Test suite
│   ├── __init__.py
│   ├── demo_test.py         # Quick demo test
│   ├── test_components.py   # Component verification
│   ├── test_simple.py       # Simple pipeline test
│   └── test_end_to_end.py   # Full pipeline test
├── models/                  # Vosk models (created after setup)
└── test_outputs/            # Test output files (created after testing)
```

## ⚙️ Configuration

Edit [src/config.py](src/config.py) to customize:

```python
# Ollama settings
OLLAMA_URL = "https://home.iot-connect.in"
OLLAMA_MODEL = "gemma3:4b"  # Change to llama3, mistral, etc.

# Audio settings
PROMPT_DEVICE_SELECTION = True  # Ask user to select audio devices on startup
BLUETOOTH_DEVICE_NAME = None    # or "JBL Flip 5", etc.

# Wake word
WAKE_WORD = "hello lamma"

# Session settings
MAX_CONTEXT_MESSAGES = 10  # Conversation history length
SESSION_TIMEOUT = 300       # Auto-end after 5 min inactivity
```

## 🔧 Troubleshooting

### Audio Issues
- **No input/output**: Check microphone permissions, try `BLUETOOTH_DEVICE_NAME = None`
- **Bluetooth not working**: Ensure device is paired and connected to Windows

### Ollama Issues
- **Connection failed**: Verify Ollama is running at the configured URL
- **Model not found**: Pull the model with `ollama pull gemma3`

### Installation Issues
- **PyAudio fails on Windows**: Install from wheel file (see [QUICKSTART.md](QUICKSTART.md))
- **Vosk model missing**: Run `python setup_model.py`

## 🎨 Customization

### Select Audio Devices

When starting the assistant, you'll be prompted to select your microphone and speaker:

```bash
python main.py

# You'll see:
# [1] Yes - Let me choose devices
# [2] No  - Use default devices
```

To disable this prompt, edit [src/config.py](src/config.py):
```python
PROMPT_DEVICE_SELECTION = False  # Skip device selection prompt
```

Or test device selection separately:
```bash
python -m test.test_device_selection
```

### Change Voice
```python
# In src/voice_assistant.py, after self.tts = TextToSpeech()
self.tts.list_voices()  # See available voices
self.tts.set_voice(1)   # Select by index
```

### Adjust Speech Rate
```python
self.tts.set_rate(180)  # Words per minute (default: 150)
```

### Use Larger Vosk Model
Download from https://alphacephei.com/vosk/models and update `VOSK_MODEL_PATH` in [src/config.py](src/config.py)

## 📝 License

This project is open source and available for personal and educational use.

## 🙏 Credits

Built with:
- [Vosk](https://alphacephei.com/vosk/) - Offline speech recognition
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3) - Text-to-speech
- [Ollama](https://ollama.ai/) - Local LLM inference
