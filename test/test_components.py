"""
Test script to verify all components are working correctly
"""

import sys
from pathlib import Path


def test_imports():
    """Test if all required packages are installed"""
    print("=" * 60)
    print("TESTING IMPORTS")
    print("=" * 60)

    packages = [
        ('vosk', 'Vosk speech recognition'),
        ('sounddevice', 'Audio device interface'),
        ('numpy', 'Numerical arrays'),
        ('pyttsx3', 'Text-to-speech'),
        ('requests', 'HTTP client for Ollama'),
        ('scipy', 'Scientific computing (for beep sound)'),
    ]

    all_ok = True
    for package, description in packages:
        try:
            __import__(package)
            print(f"✓ {package:20s} - {description}")
        except ImportError:
            print(f"✗ {package:20s} - {description} [MISSING]")
            all_ok = False

    return all_ok


def test_vosk_model():
    """Test if Vosk model is available"""
    print("\n" + "=" * 60)
    print("TESTING VOSK MODEL")
    print("=" * 60)

    from src import config

    model_path = Path(config.VOSK_MODEL_PATH)

    if model_path.exists():
        print(f"✓ Model found at: {model_path}")
        return True
    else:
        print(f"✗ Model not found at: {model_path}")
        print("\n  Run: python setup_model.py")
        return False


def test_audio_devices():
    """Test audio devices"""
    print("\n" + "=" * 60)
    print("TESTING AUDIO DEVICES")
    print("=" * 60)

    try:
        import sounddevice as sd
        devices = sd.query_devices()

        print(f"✓ Found {len(devices)} audio devices:")
        for idx, device in enumerate(devices):
            status = []
            if device['max_input_channels'] > 0:
                status.append("IN")
            if device['max_output_channels'] > 0:
                status.append("OUT")

            status_str = "/".join(status) if status else "NONE"
            print(f"  [{idx}] {device['name'][:50]:50s} [{status_str}]")

        return True
    except Exception as e:
        print(f"✗ Error accessing audio devices: {e}")
        return False


def test_tts():
    """Test text-to-speech"""
    print("\n" + "=" * 60)
    print("TESTING TEXT-TO-SPEECH")
    print("=" * 60)

    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        print(f"✓ TTS engine initialized")
        print(f"  Available voices: {len(voices)}")

        return True
    except Exception as e:
        print(f"✗ Error initializing TTS: {e}")
        return False


def test_ollama_connection():
    """Test Ollama connection"""
    print("\n" + "=" * 60)
    print("TESTING OLLAMA CONNECTION")
    print("=" * 60)

    try:
        import requests
        from src import config

        url = f"{config.OLLAMA_URL}/api/tags"
        print(f"  Connecting to: {config.OLLAMA_URL}")

        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()
        models = data.get('models', [])

        print(f"✓ Connected successfully")
        print(f"  Available models: {len(models)}")

        for model in models:
            marker = " [CONFIGURED]" if model['name'] == config.OLLAMA_MODEL else ""
            print(f"    - {model['name']}{marker}")

        if not any(m['name'] == config.OLLAMA_MODEL for m in models):
            print(f"\n  ⚠ Warning: Configured model '{config.OLLAMA_MODEL}' not found")
            print(f"    Run: ollama pull {config.OLLAMA_MODEL}")

        return True

    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to Ollama at {config.OLLAMA_URL}")
        print(f"  Make sure Ollama is running and accessible")
        return False
    except Exception as e:
        print(f"✗ Error testing Ollama connection: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🧪 COMPONENT TESTING")
    print("=" * 60)
    print()

    results = []

    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Vosk Model", test_vosk_model()))
    results.append(("Audio Devices", test_audio_devices()))
    results.append(("Text-to-Speech", test_tts()))
    results.append(("Ollama Connection", test_ollama_connection()))

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:20s} {status}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 60)

    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("\nYou're ready to run: python voice_assistant.py")
    else:
        print("✗ SOME TESTS FAILED")
        print("\nPlease fix the issues above before running the voice assistant.")
        sys.exit(1)

    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
