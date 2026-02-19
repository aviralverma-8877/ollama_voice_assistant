# Wake Word Not Working? Here's How to Fix It

## Quick Diagnosis

Your wake word isn't being recognized. This is usually due to one of two issues:

1. **Microphone volume is too low** → Speech recognition doesn't work at all
2. **Wake word is hard to recognize** → Speech works, but specific wake word doesn't trigger

Let's fix both issues step by step.

---

## Step 1: Fix Microphone Volume (REQUIRED)

Before the wake word can work, basic speech recognition must work.

### Test Speech Recognition:
```bash
python -m test.test_simple_wake_word
```

### Expected Output:
- ✅ **GOOD:** "✅ SUCCESS! Recognized: [your text]"
- ❌ **BAD:** "⚠ No speech recognized"

### If You See "No speech recognized":

**You MUST increase microphone volume first:**

1. **Open Sound Settings:**
   - Run: `./open_microphone_settings.bat`
   - OR: Press `Windows + I` → System → Sound → Input

2. **Adjust Settings:**
   - Set microphone volume to **100%**
   - Enable "**Microphone Boost**" (+20dB or +30dB)
   - Temporarily disable noise suppression

3. **Test Again:**
   ```bash
   python -m test.test_simple_wake_word
   ```

4. **Keep Adjusting Until:**
   - You see text being recognized
   - Max amplitude is > 10,000 (shown in debug output)

**→ Don't proceed to Step 2 until basic speech recognition works!**

---

## Step 2: Fix Wake Word Recognition

Once basic speech recognition works, we can fix the wake word.

### Problem: "lamma" is Not a Real Word

The current wake word "hello lamma" contains "lamma" which is:
- Not a real English word
- Not in Vosk's vocabulary
- Hard for the model to recognize accurately

### Solution: Use an Easier Wake Word

Edit `src/config.py` and change the wake word:

```python
# Current (HARD to recognize):
WAKE_WORD = "hello lamma"

# Recommended (EASY to recognize):
WAKE_WORD = "hello computer"     # Best option - clear, simple
# OR
WAKE_WORD = "hello assistant"    # Professional sounding
# OR
WAKE_WORD = "hey there"          # Casual, easy
# OR
WAKE_WORD = "hello"              # Simplest (may trigger more often)
```

### Why These Work Better:
- ✅ Real English words in Vosk's vocabulary
- ✅ Clear pronunciation
- ✅ Easier for the model to match
- ✅ Lower false-negative rate

---

## Step 3: Test Wake Word Detection

After changing the wake word, test it:

```bash
python -m test.test_wake_word_live
```

This will:
1. Start continuous listening
2. Show all recognized text
3. Detect when you say the wake word

### What to Watch For:

**Scenario 1: No text appears at all**
- → Microphone volume still too low
- → Go back to Step 1

**Scenario 2: Text appears but wake word not detected**
- → Your pronunciation doesn't match
- → Try saying it differently: "hello computer" vs "hellocomputer"
- → Or choose an even simpler wake word

**Scenario 3: Wake word detected!**
- → ✅ Success! You're all set!

---

## Step 4: Run the Full Assistant

Once wake word detection works:

```bash
python main.py
```

Follow the setup prompts, then:
1. Say your wake word: "hello computer" (or whatever you chose)
2. Wait for the beep
3. Speak your question
4. Listen to the response

---

## Alternative Solutions

### Option 1: Lower the Matching Threshold

If you really want to keep "hello lamma", you can make matching more lenient.

Edit `src/wake_word_detector.py` and modify the `_matches_wake_word` method to be more permissive.

### Option 2: Use Keyword Spotting Only

Change the wake word to just match on "hello":

```python
WAKE_WORD = "hello"
```

This will trigger on any phrase containing "hello", which is easier to detect but may have more false positives.

### Option 3: Use a Different Vosk Model

Download a larger, more accurate model:
- Go to: https://alphacephei.com/vosk/models
- Download: `vosk-model-en-us-0.22` (larger, more accurate)
- Extract to `models/` folder
- Update `VOSK_MODEL_PATH` in `src/config.py`

Larger models are better at recognizing unusual words.

---

## Quick Reference Commands

```bash
# Test microphone levels
python -m test.test_microphone

# Test basic speech recognition
python -m test.test_simple_wake_word

# Test wake word detection (live)
python -m test.test_wake_word_live

# Run full assistant
python main.py

# Open microphone settings
./open_microphone_settings.bat
```

---

## Current Status Checklist

Use this to track your progress:

- [ ] Microphone volume increased to 100%
- [ ] Microphone Boost enabled (+20dB or +30dB)
- [ ] Basic speech recognition working (test shows recognized text)
- [ ] Wake word changed to real English words
- [ ] Wake word detection working (test detects the wake word)
- [ ] Full assistant running and responding

---

## Still Not Working?

If you've followed all steps and it still doesn't work:

1. **Check the saved recording:**
   ```bash
   python -m test.test_save_recording
   ```
   Play `test_outputs/test_recording.wav` - can you hear your voice clearly?

2. **Try a different microphone:**
   ```bash
   python main.py
   ```
   Choose option 1 to select audio devices manually

3. **Check for conflicting applications:**
   - Close Zoom, Teams, Discord
   - These apps may lock the microphone

4. **Update audio drivers:**
   - Open Device Manager
   - Update "Sound, video and game controllers"

5. **Test with large Vosk model:**
   - Download a larger model for better accuracy
   - See "Option 3" above

---

## Understanding the Debug Output

When you run tests, you'll see output like:

```
Audio shape: (80000, 1), dtype: int16
Audio range: min=-2589.0000, max=2589.0000
⚠ Low audio level detected (2589). Applying 3.9x gain...
```

**What this means:**
- `max=2589` → Your audio level
- **Too low:** < 3,000 (automatic gain applied)
- **Good:** 10,000-30,000 (no gain needed)
- **Perfect:** > 20,000 (excellent signal)

If you consistently see "Low audio level detected", your Windows microphone volume needs to be increased.

---

## Summary

**The fix is usually simple:**

1. **Increase microphone volume in Windows to 100%**
2. **Change wake word to "hello computer" instead of "hello lamma"**
3. **Test again**

That's it! These two changes solve 95% of wake word issues.
