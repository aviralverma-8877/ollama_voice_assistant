"""
Test microphone recording functionality
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sounddevice as sd
import numpy as np
import time

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def test_microphone():
    """Test microphone recording with detailed diagnostics"""
    print("\n" + "=" * 70)
    print("🎤 MICROPHONE DIAGNOSTIC TEST")
    print("=" * 70)

    # List all devices
    print("\n📋 Available Audio Devices:")
    devices = sd.query_devices()
    for idx, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            default_marker = " [DEFAULT INPUT]" if idx == sd.default.device[0] else ""
            print(f"  [{idx}] {device['name']}{default_marker}")
            print(f"      Max Input Channels: {device['max_input_channels']}")
            print(f"      Default Sample Rate: {device['default_samplerate']}")

    # Get default input device
    try:
        default_input = sd.default.device[0]
        default_device_name = devices[default_input]['name'] if isinstance(default_input, int) else "System Default"
        print(f"\n✓ Using default input device: {default_device_name}")
    except:
        default_device_name = "Unknown"
        print("\n⚠ Could not detect default input device")

    # Test 1: Quick recording test
    print("\n" + "-" * 70)
    print("TEST 1: Quick Recording (2 seconds)")
    print("-" * 70)
    print("Recording will start in 3 seconds...")
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print("\n🔴 RECORDING NOW - Please speak!")

    try:
        # Wait for Bluetooth latency
        time.sleep(0.1)

        sample_rate = 16000
        duration = 2.0

        audio = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            device=None,  # Use default
            dtype='float32'
        )
        sd.wait()

        print("✓ Recording complete")

        # Analyze the recording
        max_amplitude = np.max(np.abs(audio))
        mean_amplitude = np.mean(np.abs(audio))

        print(f"\n📊 Recording Analysis:")
        print(f"   Max amplitude: {max_amplitude:.6f}")
        print(f"   Mean amplitude: {mean_amplitude:.6f}")
        print(f"   Duration: {duration} seconds")
        print(f"   Sample rate: {sample_rate} Hz")
        print(f"   Total samples: {len(audio)}")

        # Check if audio was captured
        if max_amplitude < 0.001:
            print("\n❌ PROBLEM: Extremely low audio level (< 0.001)")
            print("   Possible causes:")
            print("   - Microphone is muted or volume is at 0%")
            print("   - Wrong microphone selected")
            print("   - Microphone not connected")
            print("   - Permissions issue")
        elif max_amplitude < 0.01:
            print("\n⚠ WARNING: Very low audio level (< 0.01)")
            print("   Possible causes:")
            print("   - Microphone volume is too low")
            print("   - Speaking too far from microphone")
            print("   - Background noise suppression too aggressive")
        else:
            print("\n✓ Good audio level detected!")
            print("   The microphone appears to be working correctly")

        # Offer playback
        print("\n" + "-" * 70)
        print("TEST 2: Playback Test")
        print("-" * 70)
        print("Playing back your recording in 2 seconds...")
        time.sleep(2)

        # Wait for Bluetooth latency
        time.sleep(0.1)
        sd.play(audio, sample_rate)
        sd.wait()

        print("✓ Playback complete")
        print("\nDid you hear your voice played back? If yes, microphone is working!")

    except Exception as e:
        print(f"\n❌ Error during recording: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Test 2: Check for audio stream issues
    print("\n" + "-" * 70)
    print("TEST 3: Live Audio Level Monitoring (5 seconds)")
    print("-" * 70)
    print("Monitoring microphone input levels...")
    print("Speak continuously to see if levels change\n")

    try:
        levels = []

        def callback(indata, frames, time_info, status):
            if status:
                print(f"Stream status: {status}")

            # Calculate level
            level = np.max(np.abs(indata))
            levels.append(level)

            # Show visual level indicator
            bar_length = int(level * 50)
            bar = "█" * bar_length
            print(f"\r🎤 Level: {bar:<50} {level:.4f}", end='', flush=True)

        # Wait for Bluetooth latency
        time.sleep(0.1)

        with sd.InputStream(callback=callback, channels=1, samplerate=16000):
            sd.sleep(5000)  # 5 seconds

        print("\n\n✓ Live monitoring complete")

        if levels:
            max_level = max(levels)
            avg_level = sum(levels) / len(levels)
            print(f"\n📊 Live Monitoring Results:")
            print(f"   Max level: {max_level:.6f}")
            print(f"   Average level: {avg_level:.6f}")
            print(f"   Samples collected: {len(levels)}")

            if max_level < 0.001:
                print("\n❌ No audio detected during live monitoring")
                print("   Microphone is likely not receiving any input")
            elif max_level < 0.01:
                print("\n⚠ Very low levels during live monitoring")
                print("   Try speaking louder or adjusting microphone volume")
            else:
                print("\n✓ Live audio detected successfully!")

    except Exception as e:
        print(f"\n❌ Error during live monitoring: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 70)
    print("✅ DIAGNOSTIC TEST COMPLETE")
    print("=" * 70)
    print("\n💡 Next Steps:")
    print("   1. Check Windows microphone settings")
    print("   2. Ensure microphone permissions are granted")
    print("   3. Try adjusting microphone volume/boost in Windows")
    print("   4. Test with a different microphone if available")
    print("=" * 70)

if __name__ == "__main__":
    test_microphone()
