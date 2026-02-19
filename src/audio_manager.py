"""
Audio Manager - Handles audio input/output and optional Bluetooth connections
"""

import sounddevice as sd
import numpy as np
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
                    print(f"  [{len(input_devices)}] {device['name']}")

            # List output devices
            print("\n📤 Available OUTPUT devices (Speakers):")
            output_devices = []
            for idx, device in enumerate(devices):
                if device['max_output_channels'] > 0:
                    output_devices.append((idx, device))
                    print(f"  [{len(output_devices)}] {device['name']}")

            # Select input device
            print("\n" + "-" * 70)
            while True:
                try:
                    choice = input(f"\nSelect INPUT device [1-{len(input_devices)}] or 0 for default: ").strip()
                    choice_num = int(choice)

                    if choice_num == 0:
                        self.input_device = None
                        print("✓ Using default input device")
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
            while True:
                try:
                    choice = input(f"\nSelect OUTPUT device [1-{len(output_devices)}] or 0 for default: ").strip()
                    choice_num = int(choice)

                    if choice_num == 0:
                        self.output_device = None
                        print("✓ Using default output device")
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
                print(f"  Input:  Default")

            if self.output_device is not None:
                print(f"  Output: {devices[self.output_device]['name']}")
            else:
                print(f"  Output: Default")
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

            # Print selected devices
            if self.input_device:
                print(f"  Input: {devices[self.input_device]['name']}")
            else:
                print(f"  Input: Default")

            if self.output_device:
                print(f"  Output: {devices[self.output_device]['name']}")
            else:
                print(f"  Output: Default")

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
        def audio_callback(indata, frames, time, status):
            if status:
                print(f"Audio status: {status}")

            # Convert to int16 and call the callback
            audio_chunk = (indata.copy() * 32767).astype(np.int16)

            # If callback returns False, stop the stream
            if not callback(audio_chunk):
                raise sd.CallbackAbort

        try:
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

        # Play beep
        sd.play(beep, self.sample_rate, device=self.output_device)
        sd.wait()

    def list_devices(self):
        """List all available audio devices"""
        return sd.query_devices()
