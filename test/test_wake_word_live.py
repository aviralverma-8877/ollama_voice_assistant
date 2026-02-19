"""
Live wake word detection test - continuous listening
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.audio_manager import AudioManager
from src.wake_word_detector import WakeWordDetector
import time

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def test_wake_word_live():
    """Test wake word detection with continuous listening"""
    print("\n" + "=" * 70)
    print("🎯 LIVE WAKE WORD DETECTION TEST")
    print("=" * 70)

    # Initialize components
    print("\n📋 Initializing components...")
    try:
        audio_manager = AudioManager(interactive_setup=False)
        wake_word_detector = WakeWordDetector()
        print("✓ Components initialized")
    except Exception as e:
        print(f"❌ Error initializing: {e}")
        import traceback
        traceback.print_exc()
        return

    # Instructions
    print("\n" + "-" * 70)
    print("INSTRUCTIONS")
    print("-" * 70)
    print(f"\n📌 Wake word: '{wake_word_detector.wake_word}'")
    print("\n⚠ IMPORTANT:")
    print("   1. Make sure microphone volume is set to 100% in Windows")
    print("   2. Enable 'Microphone Boost' if available")
    print("   3. Speak LOUDLY and CLEARLY")
    print("   4. Say the wake word exactly: 'hello lamma'")
    print("\n💡 Alternative wake words to try:")
    print("   - 'hello llama' (single 'm')")
    print("   - 'hello lama' (no double letters)")
    print("   - Just 'hello' (simpler)")
    print("\n   You can change WAKE_WORD in src/config.py")

    print("\n" + "-" * 70)
    print("STARTING CONTINUOUS LISTENING")
    print("-" * 70)
    print("\nThe assistant will now listen continuously for the wake word.")
    print("Press Ctrl+C to stop.")
    print("\nStarting in 3 seconds...")
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)

    try:
        print(f"\n👂 LISTENING for '{wake_word_detector.wake_word}'...")
        print("   (All recognized text will be shown below)")
        print("")

        # Start listening for wake word
        detected = wake_word_detector.listen_for_wake_word(audio_manager)

        if detected:
            print("\n" + "=" * 70)
            print("✅ SUCCESS! Wake word detected!")
            print("=" * 70)
            print("\nThe wake word detection is working correctly!")
        else:
            print("\n" + "=" * 70)
            print("⚠ Wake word not detected")
            print("=" * 70)
            print("\nPossible reasons:")
            print("  1. Microphone volume still too low")
            print("  2. Wake word pronunciation doesn't match")
            print("  3. Background noise interference")
            print("  4. Vosk model accuracy limitations")

    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("⏹ Stopped by user")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n💡 Next Steps:")
    print("   If no text was recognized at all:")
    print("   → Run: python -m test.test_microphone")
    print("   → Increase Windows microphone volume to 100%")
    print("   → Enable Microphone Boost")
    print("")
    print("   If text was recognized but wake word not detected:")
    print("   → Try simpler wake word (change in src/config.py)")
    print("   → Try saying it differently: 'hello llama' or 'hello lama'")
    print("   → Lower WAKE_WORD_THRESHOLD in src/config.py")
    print("")

if __name__ == "__main__":
    test_wake_word_live()
