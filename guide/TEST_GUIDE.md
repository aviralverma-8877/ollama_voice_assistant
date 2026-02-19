# Testing Guide

This guide explains how to test your Ollama Voice Assistant before using it with actual voice input.

## Available Test Scripts

### 1. Component Test (`test_components.py`)
**Purpose**: Verify all dependencies and components are working

**What it tests**:
- ✓ All Python packages are installed
- ✓ Vosk model is downloaded and accessible
- ✓ Audio devices are detected
- ✓ Text-to-speech engine works
- ✓ Ollama server is accessible
- ✓ Model (gemma3) is available

**Run it**:
```bash
python test_components.py
```

**When to use**: Run this first to ensure everything is set up correctly.

---

### 2. Simple Pipeline Test (`test_simple.py`)
**Purpose**: Test Ollama integration and audio response generation

**What it does**:
1. Sends text questions to Ollama (bypasses speech recognition)
2. Gets responses from Ollama
3. Converts responses to speech
4. Saves response audio as WAV files
5. Saves response text files

**Run it**:
```bash
python test_simple.py
```

**Output**:
- `test_outputs/response_1_text.txt` - Response text
- `test_outputs/response_1_audio.wav` - Response audio (if supported)
- Similar files for each test question

**When to use**: Test Ollama integration and verify responses are being generated correctly.

---

### 3. End-to-End Test (`test_end_to_end.py`)
**Purpose**: Test the complete pipeline including speech generation

**What it does**:
1. Generates speech from test question using TTS
2. Saves input audio
3. Processes with STT (speech-to-text)
4. Sends recognized text to Ollama
5. Gets response
6. Converts response to speech
7. Saves response audio

**Run it**:
```bash
python test_end_to_end.py
```

**Output**:
- `test_outputs/input_question.wav` - Synthesized question audio
- `test_outputs/response_audio.wav` - Response audio

**When to use**: Test the complete pipeline to ensure all components work together.

**Note**: Due to pyttsx3 limitations, audio file generation may not work on all systems. The script will fall back to playing audio through speakers.

---

## Recommended Testing Workflow

### First Time Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download Vosk model
python setup_model.py

# 3. Verify everything is set up
python test_components.py

# 4. Test Ollama integration
python test_simple.py

# 5. (Optional) Test full pipeline
python test_end_to_end.py
```

### After Configuration Changes
```bash
# Test components after changing config
python test_components.py

# Test Ollama after changing model/URL
python test_simple.py
```

---

## Understanding Test Output

### Success Indicators
- ✓ Green checkmarks indicate successful steps
- Files created in `test_outputs/` directory
- Audio plays through speakers
- Ollama responses are coherent

### Failure Indicators
- ✗ Red X marks indicate failures
- ⚠ Warning symbols indicate partial success
- Error messages with stack traces

---

## Common Issues

### Ollama Connection Failed
```
✗ Cannot connect to Ollama at https://home.iot-connect.in
```

**Solutions**:
1. Check Ollama is running: `curl https://home.iot-connect.in/api/tags`
2. Verify URL in [config.py](config.py)
3. Check network connection

### Model Not Found
```
⚠ Warning: Model 'gemma3' not found in available models
```

**Solutions**:
1. Pull the model: `ollama pull gemma3`
2. Or change `OLLAMA_MODEL` in [config.py](config.py) to an available model

### Audio File Not Saved
```
⚠ Could not save audio file
  Playing through speakers instead...
```

**This is normal**: pyttsx3 doesn't support file saving on all systems. The response will play through speakers instead.

**Alternatives**:
- Use gTTS (requires internet) instead of pyttsx3
- Install espeak or festival TTS engines
- Accept speaker-only output

### Vosk Model Missing
```
❌ Vosk model not found at: models/vosk-model-small-en-us-0.15
```

**Solution**:
```bash
python setup_model.py
```

---

## Interpreting Results

### Good Test Results
```
✅ TEST COMPLETED

✓ Processed 3 questions successfully

  Question 1: What is the capital of France?
    Response length: 156 chars
    Text file: test_outputs/response_1_text.txt
    Audio file: test_outputs/response_1_audio.wav
```

This means:
- Ollama is working correctly
- Responses are being generated
- Text-to-speech is functional
- Files are being saved

### Check Response Quality
Open the text files in `test_outputs/` and verify:
- Responses are coherent and accurate
- Language is natural
- Responses are appropriate length

---

## Next Steps

After successful testing:

1. **Run the full assistant**:
   ```bash
   python voice_assistant.py
   ```

2. **Test with voice**:
   - Say "hello lamma"
   - Wait for beep
   - Ask a question
   - Listen to response

3. **Review output files** in `test_outputs/` to understand how the system processes queries

---

## Troubleshooting Tests

### Tests hang or freeze
- Press `Ctrl+C` to interrupt
- Check if Ollama is responding (may be slow on first request)
- Try reducing complexity in `test_simple.py`

### No audio output during tests
- Check speaker volume
- Verify audio devices in system settings
- Try setting `BLUETOOTH_DEVICE_NAME = None` in config.py

### ImportError for modules
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

---

For more help, see the main [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md).
