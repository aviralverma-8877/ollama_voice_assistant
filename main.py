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
from src.web_server import start_web_server
from src import config


def configure_ollama_url() -> str:
    """
    Prompt user to configure Ollama API URL

    Returns:
        Configured Ollama URL, or default if not configured
    """
    print("\n" + "=" * 70)
    print("🔗 Ollama API Configuration")
    print("=" * 70)

    print(f"\nℹ️  Current Ollama URL: {config.OLLAMA_URL}")
    print("\nDo you want to configure a custom Ollama URL?")
    print("  [1] Yes - Let me configure")
    print("  [2] No  - Use default (localhost)")

    while True:
        try:
            choice = input("\nYour choice [1/2]: ").strip()
            if choice == '2':
                print(f"✓ Using default URL: {config.OLLAMA_URL}")
                return config.OLLAMA_URL
            elif choice == '1':
                break
            print("❌ Please enter 1 or 2")
        except KeyboardInterrupt:
            print(f"\n\n✓ Using default URL: {config.OLLAMA_URL}")
            return config.OLLAMA_URL

    # Let user configure URL
    print("\n" + "-" * 70)
    print("\nCommon Ollama URLs:")
    print("  • Local:  http://localhost:11434 (default)")
    print("  • Remote: http://your-server-ip:11434")
    print("  • Custom: https://your-domain.com")

    while True:
        try:
            custom_url = input("\nEnter Ollama URL (or press Enter for default): ").strip()

            if not custom_url:
                print(f"✓ Using default URL: {config.OLLAMA_URL}")
                return config.OLLAMA_URL

            # Basic validation
            if not (custom_url.startswith('http://') or custom_url.startswith('https://')):
                print("❌ URL must start with http:// or https://")
                continue

            # Test connection
            print(f"\n🔍 Testing connection to {custom_url}...")
            temp_url = config.OLLAMA_URL
            config.OLLAMA_URL = custom_url

            try:
                models = OllamaClient.get_available_models()
                if models is not None:
                    print(f"✓ Connection successful! Found {len(models)} model(s)")
                    return custom_url
                else:
                    print("⚠ Could not connect to Ollama server")
                    config.OLLAMA_URL = temp_url

                    retry = input("\nTry another URL? [y/n]: ").strip().lower()
                    if retry != 'y':
                        print(f"✓ Using default URL: {config.OLLAMA_URL}")
                        return config.OLLAMA_URL
            except Exception as e:
                print(f"⚠ Connection failed: {e}")
                config.OLLAMA_URL = temp_url

                retry = input("\nTry another URL? [y/n]: ").strip().lower()
                if retry != 'y':
                    print(f"✓ Using default URL: {config.OLLAMA_URL}")
                    return config.OLLAMA_URL

        except KeyboardInterrupt:
            print(f"\n\n✓ Using default URL: {config.OLLAMA_URL}")
            return config.OLLAMA_URL


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
        # Ask user to select mode
        print("\n" + "=" * 70)
        print("🎙️  VOICE ASSISTANT - MODE SELECTION")
        print("=" * 70)
        print("\nHow would you like to use the voice assistant?")
        print("  [1] CLI Mode  - Use microphone directly in terminal")
        print("  [2] Web Mode  - Launch web server with browser interface")

        mode_choice = None
        while True:
            try:
                choice = input("\nYour choice [1/2]: ").strip()
                if choice in ['1', '2']:
                    mode_choice = choice
                    break
                print("❌ Please enter 1 or 2")
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                sys.exit(0)

        # Configure Ollama URL if enabled
        if config.PROMPT_OLLAMA_URL_SELECTION:
            ollama_url = configure_ollama_url()
            config.OLLAMA_URL = ollama_url

        # Web Server Mode
        if mode_choice == '2':
            print("\n🌐 Starting web server mode...")

            # Select model if enabled
            selected_model = None
            if config.PROMPT_MODEL_SELECTION:
                selected_model = select_ollama_model()

            # Get server settings
            print("\n" + "=" * 70)
            print("🌐 Web Server Configuration")
            print("=" * 70)

            host = "0.0.0.0"  # Listen on all network interfaces
            port = 5000

            print(f"\nDefault settings:")
            print(f"  Host: {host} (accessible on local network)")
            print(f"  Port: {port}")
            print("\nUse custom settings?")
            print("  [1] Yes - Let me configure")
            print("  [2] No  - Use defaults")

            try:
                config_choice = input("\nYour choice [1/2]: ").strip()
                if config_choice == '1':
                    try:
                        custom_host = input(f"Enter host (default: {host}): ").strip()
                        if custom_host:
                            host = custom_host

                        custom_port = input(f"Enter port (default: {port}): ").strip()
                        if custom_port:
                            port = int(custom_port)
                    except ValueError:
                        print("⚠ Invalid port, using default")
            except KeyboardInterrupt:
                print("\n\n✓ Using default settings")

            # Start web server
            start_web_server(model=selected_model, host=host, port=port)
            return

        # CLI Mode (original behavior)
        print("\n💻 Starting CLI mode...")

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
