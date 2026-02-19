"""
Test Script - Show Default Audio Devices

This script shows which devices are configured as system defaults
"""

import sys
import sounddevice as sd

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


def main():
    """Show default audio devices"""
    print("=" * 70)
    print("🎧 SYSTEM DEFAULT AUDIO DEVICES")
    print("=" * 70)

    try:
        devices = sd.query_devices()

        # Get default devices
        default_input = sd.default.device[0]
        default_output = sd.default.device[1]

        print("\n📥 Default INPUT device (Microphone):")
        if isinstance(default_input, int) and default_input < len(devices):
            device_info = devices[default_input]
            print(f"   Index: {default_input}")
            print(f"   Name:  {device_info['name']}")
            print(f"   Channels: {device_info['max_input_channels']}")
            print(f"   Sample Rate: {device_info['default_samplerate']} Hz")
        else:
            print(f"   {default_input}")

        print("\n📤 Default OUTPUT device (Speaker):")
        if isinstance(default_output, int) and default_output < len(devices):
            device_info = devices[default_output]
            print(f"   Index: {default_output}")
            print(f"   Name:  {device_info['name']}")
            print(f"   Channels: {device_info['max_output_channels']}")
            print(f"   Sample Rate: {device_info['default_samplerate']} Hz")
        else:
            print(f"   {default_output}")

        print("\n" + "=" * 70)
        print("\nℹ️  These are the devices that will be used when you")
        print("   select option [0] or [2] (default) in the assistant.")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Error querying default devices: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
