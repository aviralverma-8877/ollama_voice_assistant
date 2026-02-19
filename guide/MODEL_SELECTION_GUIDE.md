# Ollama Model Selection Guide

This guide explains how to use the interactive Ollama model selection feature.

## Overview

When starting the voice assistant, you can now select which Ollama model to use from all available models on your server. This is useful when you have multiple models installed and want to switch between them.

## How It Works

### Starting the Assistant

When you run `python main.py`, after the audio device selection, you'll see:

```
======================================================================
🤖 Ollama Model Selection
======================================================================

🔍 Fetching available models from https://home.iot-connect.in...

📦 Available models (3):
  [1] llama2:latest
  [2] gemma3:4b [CURRENT]
  [3] mistral:latest

ℹ️  Current model: gemma3:4b

Do you want to select a different model?
  [1] Yes - Let me choose a model
  [2] No  - Use current model

Your choice [1/2]:
```

### Option 1: Keep Current Model

If you choose **[2] No**, the assistant will use the model configured in `src/config.py`:

```
Your choice [1/2]: 2

✓ Using current model: gemma3:4b
```

### Option 2: Select Different Model

If you choose **[1] Yes**, you can select from available models:

```
Your choice [1/2]: 1

----------------------------------------------------------------------

Select model [1-3] or 0 for current: 3

✓ Selected model: mistral:latest
```

## Configuration

### Disable the Prompt

If you don't want to be prompted every time, edit [src/config.py](src/config.py):

```python
PROMPT_MODEL_SELECTION = False  # Skip model selection prompt
```

### Set Default Model

Change the default model in [src/config.py](src/config.py):

```python
OLLAMA_MODEL = "llama3:latest"  # Your preferred model
```

## Testing Model Selection

### List Available Models

See which models are available on your Ollama server:

```bash
python -m test.test_model_selection
```

This shows:
- All available models
- Model sizes
- Last modified dates
- Which model is currently configured

Example output:
```
======================================================================
🤖 AVAILABLE OLLAMA MODELS
======================================================================

🔍 Connecting to: https://home.iot-connect.in

✅ Found 3 model(s):

  [1] llama2:latest
       Size: 3.8 GB
       Modified: 2026-02-15T10:30:00

  [2] gemma3:4b [CURRENT]
       Size: 3.3 GB
       Modified: 2026-02-19T11:56:15

  [3] mistral:latest
       Size: 4.1 GB
       Modified: 2026-02-18T14:22:00

======================================================================

ℹ️  Current configured model: gemma3:4b
   (Set in src/config.py)
======================================================================
```

## Common Scenarios

### Scenario 1: Try a Different Model

```
Your choice [1/2]: 1

Select model [1-3]: 3  # Try mistral

✓ Selected model: mistral:latest

# Assistant now uses mistral for this session
```

### Scenario 2: Stick with Current

```
Your choice [1/2]: 2  # Use current

✓ Using current model: gemma3:4b
```

### Scenario 3: Quick Default Selection

```
Select model [1-3] or 0 for current: 0

✓ Using current model: gemma3:4b
```

## Model Selection Features

### Smart Display
- **Current marker**: Shows `[CURRENT]` next to the configured model
- **Model info**: Displays model name as shown in Ollama
- **Quick selection**: Option 0 always uses the current/default model

### Availability Check
- Queries Ollama server in real-time
- Shows only installed models
- Handles connection errors gracefully

### Persistent Configuration
- Selected model applies to current session only
- To change permanently, edit `src/config.py`
- Each run can use a different model

## Troubleshooting

### Issue: No Models Found

**Symptoms:**
```
❌ Could not fetch models from server
```

**Solutions:**
1. Check Ollama is running: `ollama list`
2. Verify URL in `src/config.py`
3. Test connection: `curl https://home.iot-connect.in/api/tags`

### Issue: Connection Timeout

**Possible causes:**
- Ollama server not accessible
- Network issues
- Incorrect URL

**Solution:**
- Verify `OLLAMA_URL` in `src/config.py`
- Test with: `python -m test.test_model_selection`

### Issue: Want to Skip Prompt

**Solution:** Edit `src/config.py`:
```python
PROMPT_MODEL_SELECTION = False
```

## Understanding Model Names

### Format: `name:tag`

- **llama2:latest** - Latest version of Llama 2
- **gemma3:4b** - Gemma 3 with 4 billion parameters
- **mistral:7b** - Mistral with 7 billion parameters

### Common Tags
- `latest` - Most recent version
- `7b`, `13b`, `70b` - Parameter count (billions)
- `instruct` - Instruction-tuned variant
- `chat` - Chat-optimized variant

## Pull New Models

To add models to your Ollama server:

```bash
# Pull a model
ollama pull llama3

# Pull specific tag
ollama pull mistral:7b-instruct

# List installed models
ollama list
```

Then restart the assistant to see the new models.

## Model Selection vs Configuration

### When to Use Model Selection

Use interactive selection when:
- Testing different models
- Comparing model performance
- One-time model change
- Experimenting with new models

### When to Update Configuration

Update `src/config.py` when:
- You found your preferred model
- You want consistent behavior
- Setting up for production
- Want to skip the prompt

## Examples

### Example 1: First-Time User

```bash
$ python main.py

# Audio device selection...

🤖 Ollama Model Selection

Your choice [1/2]: 2  # Keep current model

# Quickest option for first-time users
```

### Example 2: Model Comparison

```bash
$ python main.py

Your choice [1/2]: 1

Select model: 1  # Try llama2

# Test with llama2, then restart and try another
```

### Example 3: Production Setup

Edit `src/config.py`:
```python
OLLAMA_MODEL = "mistral:latest"
PROMPT_MODEL_SELECTION = False  # No prompt
```

```bash
$ python main.py

# Goes straight to assistant with mistral
```

## Configuration Options

### Option 1: Always Prompt (Default)

`src/config.py`:
```python
PROMPT_MODEL_SELECTION = True  # Ask user on startup
OLLAMA_MODEL = "gemma3:4b"     # Default/fallback
```

### Option 2: Never Prompt

`src/config.py`:
```python
PROMPT_MODEL_SELECTION = False  # Use configured model
OLLAMA_MODEL = "llama3:latest"  # Always use this
```

## Benefits

1. **Flexibility** - Switch models without editing config
2. **Experimentation** - Easy to test different models
3. **Comparison** - Try multiple models in one session
4. **Transparency** - See all available models
5. **Quick Default** - Fast option to use current model
6. **Real-time List** - Always shows currently installed models

## Summary

The model selection feature gives you control over which Ollama model powers the assistant:

- ✅ **Easy to use** - Simple numbered menu
- ✅ **Flexible** - Change models per session
- ✅ **Smart** - Shows current model
- ✅ **Configurable** - Can be enabled/disabled
- ✅ **Real-time** - Queries server for available models
- ✅ **Optional** - Quick option to keep current model

For most users, option [2] (keep current) works great. Use model selection when you want to experiment with different models or compare their performance.
