#!/usr/bin/env python3
"""
Ollama Voice Assistant - Main Entry Point

Run this script to start the voice assistant:
    python main.py
"""

import sys
import os

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

from src.voice_assistant import VoiceAssistant
from src import config


def main():
    """Entry point for the voice assistant"""
    try:
        interactive_setup = False

        # Ask user if they want to select audio devices (if enabled in config)
        if config.PROMPT_DEVICE_SELECTION:
            print("\n" + "=" * 70)
            print("🎧 Audio Device Setup")
            print("=" * 70)
            print("\nDo you want to select audio devices (microphone/speaker)?")
            print("  [1] Yes - Let me choose devices")
            print("  [2] No  - Use default devices")

            while True:
                try:
                    choice = input("\nYour choice [1/2]: ").strip()
                    if choice in ['1', '2']:
                        interactive_setup = (choice == '1')
                        break
                    print("❌ Please enter 1 or 2")
                except KeyboardInterrupt:
                    print("\n\n👋 Goodbye!")
                    sys.exit(0)

        # Initialize and run assistant
        assistant = VoiceAssistant(interactive_audio_setup=interactive_setup)
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
