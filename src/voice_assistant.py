"""
Ollama Voice Assistant - Main Program

A voice-activated assistant that uses:
- Vosk for wake word detection and speech-to-text
- pyttsx3 for text-to-speech
- Ollama for LLM inference
"""

import sys
import time
from datetime import datetime
from .audio_manager import AudioManager
from .wake_word_detector import WakeWordDetector
from .speech_to_text import SpeechToText
from .text_to_speech import TextToSpeech
from .ollama_client import OllamaClient
from . import config


class VoiceAssistant:
    """Main voice assistant controller"""

    def __init__(self, interactive_audio_setup: bool = False, model: str = None):
        """
        Initialize all components

        Args:
            interactive_audio_setup: If True, prompt user to select audio devices
            model: Ollama model name to use (uses config default if not provided)
        """
        print("=" * 60)
        print("🎙️  OLLAMA VOICE ASSISTANT")
        print("=" * 60)

        try:
            # Initialize components
            self.audio_manager = AudioManager(interactive_setup=interactive_audio_setup)
            self.wake_word_detector = WakeWordDetector()
            self.stt = SpeechToText()
            self.tts = TextToSpeech()
            self.ollama = OllamaClient(model=model)

            # Session state
            self.session_active = False
            self.session_start_time = None

            print("\n" + "=" * 60)
            print("✓ All components initialized successfully!")
            print("=" * 60)

        except Exception as e:
            print(f"\n❌ Failed to initialize voice assistant: {e}")
            sys.exit(1)

    def run(self):
        """Main loop - listen for wake word and handle conversations"""
        # Test Ollama connection first
        if not self.ollama.test_connection():
            print("\n❌ Cannot connect to Ollama. Please check:")
            print(f"   1. Ollama is running")
            print(f"   2. URL is correct: {config.OLLAMA_URL}")
            print(f"   3. Model is available: {config.OLLAMA_MODEL}")
            return

        print("\n🚀 Voice Assistant is ready!")
        print(f"   Say '{config.WAKE_WORD}' to activate")
        print("\n" + "-" * 60 + "\n")

        try:
            while True:
                # Listen for wake word
                if self.wake_word_detector.listen_for_wake_word(self.audio_manager):
                    self.handle_interaction()
                else:
                    # Wake word detection stopped (e.g., Ctrl+C)
                    break

        except KeyboardInterrupt:
            print("\n\n👋 Voice assistant stopped by user")
        except Exception as e:
            print(f"\n❌ Error in main loop: {e}")
            import traceback
            traceback.print_exc()

    def handle_interaction(self):
        """Handle a single voice interaction"""
        try:
            # Play beep to indicate listening
            print("\n🔔 *beep*")
            self.audio_manager.play_beep()

            # Listen for user speech
            user_speech = self.stt.listen_for_speech(
                self.audio_manager,
                timeout=10.0,
                silence_threshold=2.0
            )

            if not user_speech:
                print("❌ No speech detected")
                self.tts.speak("I didn't hear anything. Please try again.")
                return

            print(f"\n💭 You said: {user_speech}")

            # Check for exit commands
            if self._is_exit_command(user_speech):
                print("\n👋 Ending session...")
                self.tts.speak("Goodbye!")
                self.ollama.clear_context()
                self.session_active = False
                return

            # Get response from Ollama
            print("\n🤔 Thinking...")
            response = self.ollama.chat(user_speech, maintain_context=True)

            if response:
                print(f"\n🤖 Assistant: {response}\n")

                # Speak the response
                self.tts.speak(response)

                # Update session state
                if not self.session_active:
                    self.session_active = True
                    self.session_start_time = datetime.now()

                # Show context size
                context_size = self.ollama.get_context_size()
                print(f"\n📊 Context: {context_size // 2} exchanges in history")
            else:
                print("\n❌ No response from Ollama")
                self.tts.speak("Sorry, I couldn't generate a response.")

        except Exception as e:
            print(f"\n❌ Error during interaction: {e}")
            import traceback
            traceback.print_exc()
            self.tts.speak("Sorry, an error occurred. Please try again.")

        finally:
            # Ready for next wake word
            print("\n" + "-" * 60)
            print(f"👂 Listening for wake word: '{config.WAKE_WORD}'...")
            print("-" * 60 + "\n")

    def _is_exit_command(self, text: str) -> bool:
        """
        Check if the user wants to exit

        Args:
            text: User's speech text

        Returns:
            True if exit command detected
        """
        exit_phrases = [
            'goodbye', 'bye', 'exit', 'quit', 'stop',
            'end session', 'that\'s all', 'thank you bye'
        ]

        text_lower = text.lower()
        return any(phrase in text_lower for phrase in exit_phrases)


def main():
    """Entry point"""
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
