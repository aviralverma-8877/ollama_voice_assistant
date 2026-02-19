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
from src.ollama_client import OllamaClient
from src.audio_manager import AudioManager
from src import config


def select_ollama_model() -> str:
    """
    Prompt user to select an Ollama model

    Returns:
        Selected model name, or configured default if selection skipped/failed
    """
    print("\n" + "=" * 70)
    print("🤖 Ollama Model Selection")
    print("=" * 70)

    # Fetch available models
    print(f"\n🔍 Fetching available models from {config.OLLAMA_URL}...")
    models = OllamaClient.get_available_models()

    if not models:
        print("⚠ Could not fetch models from server")
        print(f"Using configured model: {config.OLLAMA_MODEL}")
        return config.OLLAMA_MODEL

    # Show available models
    print(f"\n📦 Available models ({len(models)}):")
    for idx, model in enumerate(models, 1):
        model_name = model['name']
        # Mark the configured model as default
        default_marker = " [CURRENT]" if model_name == config.OLLAMA_MODEL else ""
        print(f"  [{idx}] {model_name}{default_marker}")

    # Ask user if they want to select
    print(f"\nℹ️  Current model: {config.OLLAMA_MODEL}")
    print("\nDo you want to select a different model?")
    print("  [1] Yes - Let me choose a model")
    print("  [2] No  - Use current model")

    while True:
        try:
            choice = input("\nYour choice [1/2]: ").strip()
            if choice == '2':
                print(f"✓ Using current model: {config.OLLAMA_MODEL}")
                return config.OLLAMA_MODEL
            elif choice == '1':
                break
            print("❌ Please enter 1 or 2")
        except KeyboardInterrupt:
            print(f"\n\n✓ Using current model: {config.OLLAMA_MODEL}")
            return config.OLLAMA_MODEL

    # Let user select model
    print("\n" + "-" * 70)
    while True:
        try:
            choice = input(f"\nSelect model [1-{len(models)}] or 0 for current: ").strip()
            choice_num = int(choice)

            if choice_num == 0:
                print(f"✓ Using current model: {config.OLLAMA_MODEL}")
                return config.OLLAMA_MODEL
            elif 1 <= choice_num <= len(models):
                selected_model = models[choice_num - 1]['name']
                print(f"✓ Selected model: {selected_model}")
                return selected_model
            else:
                print(f"❌ Please enter a number between 0 and {len(models)}")
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print(f"\n\n✓ Using current model: {config.OLLAMA_MODEL}")
            return config.OLLAMA_MODEL


def main():
    """Entry point for the voice assistant"""
    try:
        interactive_setup = False
        selected_model = None
        test_devices = False

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

        # Ask user if they want to test audio devices (if enabled in config)
        if config.PROMPT_DEVICE_TEST:
            print("\n" + "=" * 70)
            print("🎧 Audio Device Test")
            print("=" * 70)
            print("\nDo you want to test your microphone and speaker?")
            print("  [1] Yes - Test my devices")
            print("  [2] No  - Skip test")

            while True:
                try:
                    choice = input("\nYour choice [1/2]: ").strip()
                    if choice == '1':
                        test_devices = True
                        print("✓ Device test will run after initialization")
                        break
                    elif choice == '2':
                        print("✓ Skipping device test")
                        break
                    else:
                        print("❌ Please enter 1 or 2")
                except KeyboardInterrupt:
                    print("\n\n✓ Skipping device test")
                    break

        # Ask user if they want to select Ollama model (if enabled in config)
        if config.PROMPT_MODEL_SELECTION:
            selected_model = select_ollama_model()

        # Initialize and run assistant
        assistant = VoiceAssistant(
            interactive_audio_setup=interactive_setup,
            model=selected_model,
            test_devices=test_devices
        )
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
