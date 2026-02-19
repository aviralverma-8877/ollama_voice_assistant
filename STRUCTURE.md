# Project Structure

This document explains the reorganized project structure.

## Directory Layout

```
ollama-voise-assistant/
├── main.py                     # Main entry point - START HERE
├── setup_model.py              # Utility to download Vosk models
├── requirements.txt            # Python dependencies
│
├── src/                        # Source code directory
│   ├── __init__.py
│   ├── config.py               # Configuration (Ollama URL, model, etc.)
│   ├── voice_assistant.py      # Main assistant orchestrator
│   ├── audio_manager.py        # Audio I/O and Bluetooth handling
│   ├── wake_word_detector.py   # Wake word detection logic
│   ├── speech_to_text.py       # Speech-to-text using Vosk
│   ├── text_to_speech.py       # Text-to-speech using pyttsx3
│   └── ollama_client.py        # Ollama API client
│
├── test/                       # Test suite directory
│   ├── __init__.py
│   ├── demo_test.py            # Quick demo test (start here for testing)
│   ├── test_components.py      # Verify all components work
│   ├── test_simple.py          # Simple pipeline test
│   └── test_end_to_end.py      # Full end-to-end test
│
├── models/                     # Vosk models (created by setup_model.py)
├── test_outputs/               # Test output files (audio, text)
│
└── docs/                       # Documentation
    ├── README.md
    ├── QUICKSTART.md
    ├── TEST_GUIDE.md
    └── TESTING_SUMMARY.md
```

## Key Files

### Entry Points

- **`main.py`** - Start the voice assistant
  ```bash
  python main.py
  ```

- **`test/demo_test.py`** - Quick test with Ollama
  ```bash
  python -m test.demo_test
  ```

- **`setup_model.py`** - Download Vosk model
  ```bash
  python setup_model.py
  ```

### Configuration

- **`src/config.py`** - Main configuration file
  - Ollama URL and model
  - Wake word settings
  - Audio settings
  - Bluetooth device configuration

### Source Code (`src/`)

All core functionality is in the `src/` directory:

1. **`voice_assistant.py`** - Main orchestrator
   - Initializes all components
   - Runs the main loop
   - Handles user interactions

2. **`audio_manager.py`** - Audio handling
   - Audio input/output
   - Bluetooth device support
   - Beep sound generation

3. **`wake_word_detector.py`** - Wake word detection
   - Listens for "hello lamma"
   - Uses Vosk for recognition
   - Fuzzy matching support

4. **`speech_to_text.py`** - Speech recognition
   - Vosk-based STT
   - Stream processing
   - Silence detection

5. **`text_to_speech.py`** - Speech synthesis
   - pyttsx3-based TTS
   - Voice customization
   - Rate and volume control

6. **`ollama_client.py`** - Ollama integration
   - API communication
   - Context management
   - Error handling

### Tests (`test/`)

All test files are in the `test/` directory:

1. **`demo_test.py`** - Quick demonstration
   - Tests Ollama connection
   - Generates response
   - Saves text and audio

2. **`test_components.py`** - Component verification
   - Checks all dependencies
   - Tests Ollama connection
   - Verifies audio devices
   - Tests Vosk model

3. **`test_simple.py`** - Pipeline test
   - Tests multiple questions
   - Saves all responses
   - Audio file generation

4. **`test_end_to_end.py`** - Full pipeline
   - Complete workflow test
   - TTS → STT → Ollama → TTS
   - Audio file handling

## Running the Project

### First Time Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download Vosk model
python setup_model.py

# 3. Configure (optional)
# Edit src/config.py to customize settings

# 4. Test (recommended)
python -m test.demo_test

# 5. Run the assistant
python main.py
```

### Running Tests

```bash
# Quick demo test
python -m test.demo_test

# Component verification
python -m test.test_components

# Simple pipeline test
python -m test.test_simple

# Full end-to-end test
python -m test.test_end_to_end
```

### Running the Voice Assistant

```bash
# Start the assistant
python main.py
```

Then:
1. Say "hello lamma"
2. Wait for beep
3. Speak your question
4. Listen to response

## Import Structure

### Within `src/` (relative imports)

```python
# In src/voice_assistant.py
from .audio_manager import AudioManager
from .ollama_client import OllamaClient
from . import config
```

### From tests (absolute imports)

```python
# In test/demo_test.py
from src.ollama_client import OllamaClient
from src import config
```

### From main.py (absolute imports)

```python
# In main.py
from src.voice_assistant import VoiceAssistant
```

## Benefits of This Structure

1. **Clear Separation** - Source code and tests are separate
2. **Easy Navigation** - Files are logically organized
3. **Clean Entry Point** - `main.py` is the obvious starting point
4. **Testability** - Tests are isolated in `test/` directory
5. **Scalability** - Easy to add new modules or tests
6. **Professional** - Follows Python best practices

## Configuration

Edit `src/config.py` to customize:

```python
# Ollama Configuration
OLLAMA_URL = "https://home.iot-connect.in"
OLLAMA_MODEL = "gemma3:4b"

# Wake Word
WAKE_WORD = "hello lamma"

# Audio Settings
SAMPLE_RATE = 16000
BLUETOOTH_DEVICE_NAME = None  # or "Your Device Name"

# Session Settings
MAX_CONTEXT_MESSAGES = 10
SESSION_TIMEOUT = 300
```

## Troubleshooting

### Import Errors

If you see import errors:
- Make sure you're in the project root directory
- Use `python -m test.demo_test` not `python test/demo_test.py`
- Ensure `src/__init__.py` and `test/__init__.py` exist

### Module Not Found

```bash
# Wrong:
cd test
python demo_test.py

# Correct:
cd ollama-voise-assistant
python -m test.demo_test
```

### Path Issues

Always run commands from the project root:
```bash
cd c:\Users\aviralv\Documents\ollama-voise-assistant
python main.py
```

## Next Steps

1. Review [QUICKSTART.md](QUICKSTART.md) for setup instructions
2. Check [TEST_GUIDE.md](TEST_GUIDE.md) for testing details
3. Read [README.md](README.md) for full documentation
4. Customize [src/config.py](src/config.py) for your setup
