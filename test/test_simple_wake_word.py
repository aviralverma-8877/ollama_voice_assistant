"""
Simple test for wake word detection and speech recognition
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.audio_manager import AudioManager
from src.speech_to_text import SpeechToText
import time

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def test_speech_recognition():
    """Test basic speech recognition"""
    print("\n" + "=" * 70)
    print("🎤 SPEECH RECOGNITION TEST")
    print("=" * 70)

    # Initialize components
    print("\n📋 Initializing components...")
    try:
        audio_manager = AudioManager(interactive_setup=False)
        stt = SpeechToText()
        print("✓ Components initialized")
    except Exception as e:
        print(f"❌ Error initializing: {e}")
        import traceback
        traceback.print_exc()
        return

    # Test speech recognition
    print("\n" + "-" * 70)
    print("TEST: Recording and transcribing speech")
    print("-" * 70)
    print("\nI will record for 5 seconds. Please speak clearly.")
    print("Try saying: 'Hello, this is a test'")
    print("\nStarting in 3 seconds...")
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)

    try:
        print("\n🔴 RECORDING NOW! Speak please...")
        audio = audio_manager.record_audio(duration=5.0)
        print("✓ Recording complete")

        print("\n🔄 Converting speech to text...")
        # Pass the actual sample rate being used
        text = stt.transcribe_audio(audio, source_sample_rate=audio_manager.sample_rate)

        if text:
            print(f"\n✅ SUCCESS! Recognized: \"{text}\"")
            print("\n🎉 Speech recognition is working!")

            # Check if it contains wake word
            wake_word = "computer"
            if wake_word in text.lower():
                print(f"\n🎯 BONUS: Detected wake word '{wake_word}' in the text!")

        else:
            print("\n⚠ No speech recognized")
            print("\nPossible issues:")
            print("  1. You need to speak louder")
            print("  2. Microphone is too far away")
            print("  3. Too much background noise")
            print("  4. Check Windows microphone settings:")
            print("     - Settings > System > Sound > Input")
            print("     - Make sure microphone volume is at least 50%")
            print("     - Try enabling 'microphone boost' if available")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_speech_recognition()
