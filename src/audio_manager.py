"""
Audio Manager - Handles audio input/output and optional Bluetooth connections
"""

import sounddevice as sd
import numpy as np
import time
from typing import Optional, Callable
from . import config


class AudioManager:
    """Manages audio input/output for the voice assistant"""

    def __init__(self, interactive_setup: bool = False):
        """
        Initialize audio manager

        Args:
            interactive_setup: If True, prompt user to select devices
        """
        self.sample_rate = config.SAMPLE_RATE
        self.channels = config.CHANNELS
        self.chunk_size = config.CHUNK_SIZE
        self.input_device = None
        self.output_device = None

        if interactive_setup:
            self._interactive_device_selection()
        else:
            self._setup_devices()

    def _interactive_device_selection(self):
        """Interactive device selection - prompt user to choose devices"""
        try:
            devices = sd.query_devices()

            # Get default devices
            try:
                default_input = sd.default.device[0]
                default_output = sd.default.device[1]
                default_input_name = devices[default_input]['name'] if isinstance(default_input, int) else "System Default"
                default_output_name = devices[default_output]['name'] if isinstance(default_output, int) else "System Default"
            except:
                default_input_name = "System Default"
                default_output_name = "System Default"

            # Show all available devices
            print("\n" + "=" * 70)
            print("AUDIO DEVICE SELECTION")
            print("=" * 70)

            # List input devices
            print("\n📥 Available INPUT devices (Microphones):")
            input_devices = []
            for idx, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    input_devices.append((idx, device))
                    default_marker = " [DEFAULT]" if (isinstance(default_input, int) and idx == default_input) else ""
                    print(f"  [{len(input_devices)}] {device['name']}{default_marker}")

            # List output devices
            print("\n📤 Available OUTPUT devices (Speakers):")
            output_devices = []
            for idx, device in enumerate(devices):
                if device['max_output_channels'] > 0:
                    output_devices.append((idx, device))
                    default_marker = " [DEFAULT]" if (isinstance(default_output, int) and idx == default_output) else ""
                    print(f"  [{len(output_devices)}] {device['name']}{default_marker}")

            # Select input device
            print("\n" + "-" * 70)
            print(f"ℹ️  Default input: {default_input_name}")
            while True:
                try:
                    choice = input(f"\nSelect INPUT device [1-{len(input_devices)}] or 0 for default: ").strip()
                    choice_num = int(choice)

                    if choice_num == 0:
                        self.input_device = None
                        print(f"✓ Using default input device: {default_input_name}")
                        break
                    elif 1 <= choice_num <= len(input_devices):
                        device_idx, device_info = input_devices[choice_num - 1]
                        self.input_device = device_idx
                        print(f"✓ Selected: {device_info['name']}")
                        break
                    else:
                        print(f"❌ Please enter a number between 0 and {len(input_devices)}")
                except ValueError:
                    print("❌ Please enter a valid number")
                except KeyboardInterrupt:
                    print("\n\n⚠ Using default devices")
                    self.input_device = None
                    self.output_device = None
                    return

            # Select output device
            print("\n" + "-" * 70)
            print(f"ℹ️  Default output: {default_output_name}")
            while True:
                try:
                    choice = input(f"\nSelect OUTPUT device [1-{len(output_devices)}] or 0 for default: ").strip()
                    choice_num = int(choice)

                    if choice_num == 0:
                        self.output_device = None
                        print(f"✓ Using default output device: {default_output_name}")
                        break
                    elif 1 <= choice_num <= len(output_devices):
                        device_idx, device_info = output_devices[choice_num - 1]
                        self.output_device = device_idx
                        print(f"✓ Selected: {device_info['name']}")
                        break
                    else:
                        print(f"❌ Please enter a number between 0 and {len(output_devices)}")
                except ValueError:
                    print("❌ Please enter a valid number")
                except KeyboardInterrupt:
                    print("\n\n⚠ Using default devices")
                    self.output_device = None
                    return

            # Show final selection
            print("\n" + "=" * 70)
            print("SELECTED DEVICES:")
            print("=" * 70)
            if self.input_device is not None:
                print(f"  Input:  {devices[self.input_device]['name']}")
            else:
                print(f"  Input:  {default_input_name} (default)")

            if self.output_device is not None:
                print(f"  Output: {devices[self.output_device]['name']}")
            else:
                print(f"  Output: {default_output_name} (default)")
            print("=" * 70)

        except Exception as e:
            print(f"\n❌ Error during device selection: {e}")
            print("⚠ Falling back to default devices")
            self.input_device = None
            self.output_device = None

    def _setup_devices(self):
        """Setup audio devices (with optional Bluetooth)"""
        try:
            devices = sd.query_devices()
            print("\nAvailable audio devices:")
            for idx, device in enumerate(devices):
                print(f"  [{idx}] {device['name']} (In: {device['max_input_channels']}, Out: {device['max_output_channels']})")

            # If Bluetooth device is specified, try to find it
            if config.BLUETOOTH_DEVICE_NAME:
                for idx, device in enumerate(devices):
                    if config.BLUETOOTH_DEVICE_NAME.lower() in device['name'].lower():
                        if device['max_input_channels'] > 0:
                            self.input_device = idx
                        if device['max_output_channels'] > 0:
                            self.output_device = idx
                        print(f"\n✓ Found Bluetooth device: {device['name']}")
                        break

                if self.input_device is None and self.output_device is None:
                    print(f"\n⚠ Bluetooth device '{config.BLUETOOTH_DEVICE_NAME}' not found. Using default devices.")
            else:
                print("\n✓ Using default audio devices")

            # Get default device names
            try:
                default_input = sd.default.device[0]
                default_output = sd.default.device[1]
                default_input_name = devices[default_input]['name'] if isinstance(default_input, int) else "System Default"
                default_output_name = devices[default_output]['name'] if isinstance(default_output, int) else "System Default"
            except:
                default_input_name = "System Default"
                default_output_name = "System Default"

            # Print selected devices
            if self.input_device is not None:
                print(f"  Input:  {devices[self.input_device]['name']}")
            else:
                print(f"  Input:  {default_input_name} (default)")

            if self.output_device is not None:
                print(f"  Output: {devices[self.output_device]['name']}")
            else:
                print(f"  Output: {default_output_name} (default)")

        except Exception as e:
            print(f"Warning: Could not enumerate audio devices: {e}")
            print("Using default audio devices")

    def record_audio(self, duration: float = 5.0) -> np.ndarray:
        """
        Record audio for a specified duration

        Args:
            duration: Recording duration in seconds

        Returns:
            numpy array of audio samples
        """
        print(f"🎤 Recording for {duration} seconds...")
        # Wait 100ms for Bluetooth device latency
        time.sleep(0.1)
        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            device=self.input_device,
            dtype='int16'
        )
        sd.wait()
        return audio

    def record_stream(self, callback: Callable[[np.ndarray], bool], chunk_duration: float = 0.25):
        """
        Record audio stream and call callback for each chunk

        Args:
            callback: Function called with each audio chunk. Return False to stop recording.
            chunk_duration: Duration of each chunk in seconds
        """
        def audio_callback(indata, frames, time_info, status):
            if status:
                print(f"Audio status: {status}")

            # Convert to int16 and call the callback
            audio_chunk = (indata.copy() * 32767).astype(np.int16)

            # If callback returns False, stop the stream
            if not callback(audio_chunk):
                raise sd.CallbackAbort

        try:
            # Wait 100ms for Bluetooth device latency before starting stream
            time.sleep(0.1)
            with sd.InputStream(
                callback=audio_callback,
                channels=self.channels,
                samplerate=self.sample_rate,
                device=self.input_device,
                blocksize=int(chunk_duration * self.sample_rate)
            ):
                # Keep stream open until callback aborts it
                while True:
                    sd.sleep(100)
        except sd.CallbackAbort:
            pass
        except KeyboardInterrupt:
            print("\n\nStream interrupted by user")

    def play_beep(self):
        """Play a beep sound to indicate wake word detected"""
        duration = config.BEEP_DURATION
        frequency = config.BEEP_FREQUENCY

        # Generate beep sound
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        beep = np.sin(2 * np.pi * frequency * t) * 0.3  # 30% volume

        # Wait 100ms for Bluetooth device latency
        time.sleep(0.1)
        # Play beep
        sd.play(beep, self.sample_rate, device=self.output_device)
        sd.wait()

    def list_devices(self):
        """List all available audio devices"""
        return sd.query_devices()

    def test_devices(self):
        """
        Test microphone and speaker
        Records audio and plays it back
        """
        print("\n" + "=" * 70)
        print("🎧 AUDIO DEVICE TEST")
        print("=" * 70)

        # Test speaker first
        print("\n🔊 Testing speaker...")
        print("   You should hear a beep sound")
        input("\nPress Enter to play test beep...")

        try:
            self.play_beep()
            print("✓ Beep played")

            # Ask if user heard it
            while True:
                response = input("\nDid you hear the beep? [y/n]: ").strip().lower()
                if response in ['y', 'yes']:
                    print("✓ Speaker test passed")
                    break
                elif response in ['n', 'no']:
                    print("⚠ Speaker may not be working correctly")
                    print("  Check volume and device selection")
                    break
                else:
                    print("❌ Please enter 'y' or 'n'")

        except Exception as e:
            print(f"❌ Error testing speaker: {e}")
            return False

        # Test microphone
        print("\n🎤 Testing microphone...")
        print("   Speak after the beep to test your microphone")
        input("\nPress Enter to start microphone test...")

        try:
            # Play beep to signal start
            self.play_beep()

            # Record for 3 seconds
            duration = 3.0
            print(f"\n🔴 Recording for {duration} seconds...")
            print("   Speak now: Say something like 'Testing, one, two, three'")

            # Wait 100ms for Bluetooth device latency
            time.sleep(0.1)
            audio = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                device=self.input_device,
                dtype='float32'
            )
            sd.wait()

            print("✓ Recording complete")

            # Check if audio was captured
            max_amplitude = np.max(np.abs(audio))
            if max_amplitude < 0.01:
                print("\n⚠ Very low audio level detected")
                print("  Microphone may not be working or volume is too low")
            else:
                print(f"\n✓ Audio captured (level: {max_amplitude:.3f})")

                # Ask if user wants to hear playback
                response = input("\nPlay back recording? [y/n]: ").strip().lower()
                if response in ['y', 'yes']:
                    print("\n🔊 Playing back your recording...")
                    # Wait 100ms for Bluetooth device latency
                    time.sleep(0.1)
                    sd.play(audio, self.sample_rate, device=self.output_device)
                    sd.wait()
                    print("✓ Playback complete")

            print("\n✓ Microphone test complete")

        except Exception as e:
            print(f"❌ Error testing microphone: {e}")
            return False

        print("\n" + "=" * 70)
        print("✅ DEVICE TEST COMPLETE")
        print("=" * 70)

        return True
