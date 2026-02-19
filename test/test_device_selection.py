"""
Test Script - Audio Device Selection

Tests the interactive device selection feature
"""

import sys
from src.audio_manager import AudioManager


def main():
    """Test interactive device selection"""
    print("=" * 70)
    print("🧪 TESTING INTERACTIVE DEVICE SELECTION")
    print("=" * 70)

    try:
        # Test interactive device selection
        print("\n📋 This will test the device selection interface")
        print("   You'll be prompted to select input and output devices")

        audio_manager = AudioManager(interactive_setup=True)

        # Show final configuration
        print("\n✅ Device selection completed!")
        print(f"\n   Selected input device: {audio_manager.input_device}")
        print(f"   Selected output device: {audio_manager.output_device}")

        # Test beep with selected device
        print("\n🔊 Testing selected output device with beep sound...")
        print("   (You should hear a beep)")

        input("\nPress Enter to play test beep...")
        audio_manager.play_beep()

        print("\n✅ Test completed successfully!")

    except KeyboardInterrupt:
        print("\n\n⚠ Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
