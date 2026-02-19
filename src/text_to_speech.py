"""
Text-to-Speech - Converts text to speech using pyttsx3
"""

import pyttsx3
import time
from typing import Optional


class TextToSpeech:
    """Handles text-to-speech conversion using pyttsx3"""

    def __init__(self, rate: int = 150, volume: float = 0.9):
        """
        Initialize TTS engine

        Args:
            rate: Speech rate (words per minute). Default: 150
            volume: Volume level (0.0 to 1.0). Default: 0.9
        """
        self.engine = pyttsx3.init()
        self.rate = rate
        self.volume = volume

        # Configure engine
        self.engine.setProperty('rate', self.rate)
        self.engine.setProperty('volume', self.volume)

        # Get available voices
        voices = self.engine.getProperty('voices')
        print(f"\n🔊 Text-to-Speech initialized")
        print(f"   Available voices: {len(voices)}")

        # Try to set a good default voice (prefer female voices if available)
        if voices:
            # List available voices
            for idx, voice in enumerate(voices):
                print(f"   [{idx}] {voice.name} ({voice.languages})")

            # You can change this to select a different voice by index
            # self.engine.setProperty('voice', voices[1].id)

    def speak(self, text: str):
        """
        Convert text to speech and play it

        Args:
            text: The text to speak
        """
        if not text or not text.strip():
            print("⚠ No text to speak")
            return

        print(f"💬 Speaking: {text[:100]}{'...' if len(text) > 100 else ''}")

        try:
            # Wait 100ms for Bluetooth device latency
            time.sleep(0.1)
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"❌ Error during speech synthesis: {e}")

    def set_rate(self, rate: int):
        """
        Set speech rate

        Args:
            rate: Words per minute (typically 100-200)
        """
        self.rate = rate
        self.engine.setProperty('rate', rate)
        print(f"Speech rate set to {rate} WPM")

    def set_volume(self, volume: float):
        """
        Set volume level

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        self.engine.setProperty('volume', self.volume)
        print(f"Volume set to {self.volume:.1%}")

    def set_voice(self, voice_index: int):
        """
        Set voice by index

        Args:
            voice_index: Index of the voice to use
        """
        voices = self.engine.getProperty('voices')
        if 0 <= voice_index < len(voices):
            self.engine.setProperty('voice', voices[voice_index].id)
            print(f"Voice set to: {voices[voice_index].name}")
        else:
            print(f"❌ Invalid voice index. Available: 0-{len(voices)-1}")

    def list_voices(self):
        """List all available voices"""
        voices = self.engine.getProperty('voices')
        print("\nAvailable voices:")
        for idx, voice in enumerate(voices):
            print(f"  [{idx}] {voice.name}")
            print(f"       ID: {voice.id}")
            print(f"       Languages: {voice.languages}")
            print()

    def stop(self):
        """Stop the current speech"""
        try:
            self.engine.stop()
        except Exception as e:
            print(f"Error stopping speech: {e}")
