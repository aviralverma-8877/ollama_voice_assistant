"""
Test that saves recorded audio to a WAV file for inspection
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.audio_manager import AudioManager
from src.speech_to_text import SpeechToText
import numpy as np
import wave
import time

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def save_recording():
    """Record audio and save to WAV file"""
    print("\n" + "=" * 70)
    print("🎤 AUDIO RECORDING AND SAVE TEST")
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

    # Create output directory
    output_dir = "test_outputs"
    os.makedirs(output_dir, exist_ok=True)

    # Record audio
    print("\n" + "-" * 70)
    print("RECORDING TEST")
    print("-" * 70)
    print("\nI will record for 5 seconds and save to a WAV file.")
    print("Please speak LOUDLY and CLEARLY.")
    print("Try saying: 'Testing one two three, hello lamma'")
    print("\nStarting in 3 seconds...")
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)

    try:
        print("\n🔴 RECORDING NOW! SPEAK LOUDLY!")
        audio = audio_manager.record_audio(duration=5.0)
        print("✓ Recording complete")

        # Flatten if needed
        if len(audio.shape) > 1:
            audio = audio.flatten()

        # Save to WAV file
        wav_file = os.path.join(output_dir, "test_recording.wav")
        print(f"\n💾 Saving to: {wav_file}")

        with wave.open(wav_file, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(audio_manager.sample_rate)
            wf.writeframes(audio.tobytes())

        print(f"✓ Audio saved successfully")
        print(f"\n📊 Audio Info:")
        print(f"   Duration: 5.0 seconds")
        print(f"   Sample rate: {audio_manager.sample_rate} Hz")
        print(f"   Samples: {len(audio)}")
        print(f"   Max amplitude: {np.max(np.abs(audio))}")
        print(f"   Mean amplitude: {np.mean(np.abs(audio)):.2f}")

        # Try to transcribe
        print("\n🔄 Attempting transcription...")
        text = stt.transcribe_audio(audio, source_sample_rate=audio_manager.sample_rate)

        if text:
            print(f"\n✅ Transcribed text: \"{text}\"")
        else:
            print(f"\n⚠ No text recognized")
            print(f"\n💡 Please:")
            print(f"   1. Play the saved file: {wav_file}")
            print(f"   2. Verify you can hear your voice")
            print(f"   3. If you can hear it, the issue is with Vosk recognition")
            print(f"   4. If you can't hear it, increase microphone volume in Windows:")
            print(f"      - Settings > System > Sound > Input")
            print(f"      - Set microphone volume to 100%")
            print(f"      - Enable 'Microphone Boost' if available")

        print(f"\n📁 Saved file location: {os.path.abspath(wav_file)}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 70)

if __name__ == "__main__":
    save_recording()
