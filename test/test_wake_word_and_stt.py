"""
Test wake word detection and speech-to-text functionality
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.audio_manager import AudioManager
from src.wake_word_detector import WakeWordDetector
from src.speech_to_text import SpeechToText
import time

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def test_wake_word_and_stt():
    """Test wake word detection and speech-to-text"""
    print("\n" + "=" * 70)
    print("🎯 WAKE WORD & SPEECH-TO-TEXT TEST")
    print("=" * 70)

    # Initialize components
    print("\n📋 Initializing components...")
    try:
        audio_manager = AudioManager(interactive_setup=False)
        wake_word_detector = WakeWordDetector()
        stt = SpeechToText()
        print("✓ All components initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing components: {e}")
        import traceback
        traceback.print_exc()
        return

    # Test 1: Simple speech recognition without wake word
    print("\n" + "-" * 70)
    print("TEST 1: Speech Recognition (5 seconds)")
    print("-" * 70)
    print("This test will record your voice for 5 seconds and convert to text.")
    print("\nReady? Recording starts in 3 seconds...")
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print("\n🔴 RECORDING NOW!")
    print("Say something like: 'Hello, this is a test of the speech recognition system'")

    try:
        audio = audio_manager.record_audio(duration=5.0)
        print("✓ Recording complete")

        print("\n🔄 Converting speech to text...")
        text = stt.recognize(audio)

        if text:
            print(f"\n✓ Recognized text: \"{text}\"")
            print("\n✅ Speech recognition is working!")
        else:
            print("\n⚠ No speech recognized")
            print("   Possible causes:")
            print("   - Speaking too quietly")
            print("   - Background noise")
            print("   - Vosk model issues")

    except Exception as e:
        print(f"\n❌ Error during speech recognition: {e}")
        import traceback
        traceback.print_exc()

    # Test 2: Wake word detection
    print("\n" + "-" * 70)
    print("TEST 2: Wake Word Detection")
    print("-" * 70)
    print(f"Wake word: '{wake_word_detector.wake_word}'")
    print("\nThis test will record for 5 seconds and check for wake word.")
    print("\nReady? Recording starts in 3 seconds...")
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print(f"\n🔴 RECORDING NOW!")
    print(f"Say the wake word: '{wake_word_detector.wake_word}'")
    print("(Try saying it 2-3 times clearly)")

    try:
        audio = audio_manager.record_audio(duration=5.0)
        print("✓ Recording complete")

        print("\n🔄 Checking for wake word...")
        # First transcribe to see what was said
        text = stt.recognize(audio)
        print(f"\n📝 What you said: \"{text}\"")

        # Check for wake word
        detected = wake_word_detector.detect(audio, stt)

        if detected:
            print(f"\n✅ Wake word '{wake_word_detector.wake_word}' DETECTED!")
            print("   Wake word detection is working!")
        else:
            print(f"\n⚠ Wake word '{wake_word_detector.wake_word}' NOT detected")
            print(f"   But you said: \"{text}\"")
            print("\n   Possible causes:")
            print(f"   - Wake word not said clearly enough")
            print(f"   - Wake word needs to match exactly: '{wake_word_detector.wake_word}'")
            print(f"   - Try adjusting WAKE_WORD_THRESHOLD in config.py")
            print(f"   - Current threshold: {wake_word_detector.confidence_threshold}")

    except Exception as e:
        print(f"\n❌ Error during wake word detection: {e}")
        import traceback
        traceback.print_exc()

    # Test 3: Continuous listening simulation
    print("\n" + "-" * 70)
    print("TEST 3: Continuous Listening Simulation (10 seconds)")
    print("-" * 70)
    print(f"This simulates how the assistant listens for wake word.")
    print(f"\nSay '{wake_word_detector.wake_word}' anytime during the next 10 seconds")
    print("\nStarting in 3 seconds...")
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print(f"\n👂 LISTENING for wake word...")

    wake_word_count = 0
    chunks_processed = 0

    try:
        def process_chunk(audio_chunk):
            nonlocal wake_word_count, chunks_processed
            chunks_processed += 1

            # Check for wake word in this chunk
            if wake_word_detector.detect(audio_chunk, stt):
                wake_word_count += 1
                print(f"\n🎯 Wake word detected! (Total: {wake_word_count})")
                return True

            # Show we're still listening
            if chunks_processed % 4 == 0:
                print(".", end="", flush=True)

            return True  # Continue listening

        # Listen for 10 seconds in chunks
        start_time = time.time()
        while time.time() - start_time < 10:
            audio_chunk = audio_manager.record_audio(duration=1.0)
            process_chunk(audio_chunk)

        print("\n\n✓ Listening test complete")
        print(f"   Chunks processed: {chunks_processed}")
        print(f"   Wake word detected: {wake_word_count} times")

        if wake_word_count > 0:
            print("\n✅ Continuous wake word detection is working!")
        else:
            print(f"\n⚠ No wake word detected during continuous listening")
            print(f"   Try saying '{wake_word_detector.wake_word}' more clearly")

    except Exception as e:
        print(f"\n❌ Error during continuous listening: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 70)
    print("✅ TEST COMPLETE")
    print("=" * 70)
    print("\n💡 Summary:")
    print("   - If speech recognition works but wake word doesn't:")
    print("     Try adjusting WAKE_WORD_THRESHOLD in src/config.py")
    print("     (Lower value = more sensitive, Higher = more strict)")
    print(f"     Current: {wake_word_detector.confidence_threshold}")
    print("\n   - If nothing is recognized:")
    print("     Check microphone volume in Windows settings")
    print("     Speak louder and closer to the microphone")
    print("=" * 70)

if __name__ == "__main__":
    test_wake_word_and_stt()
