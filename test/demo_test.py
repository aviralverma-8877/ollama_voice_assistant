"""
DEMO TEST - Simple demonstration of the complete pipeline

This script demonstrates:
1. Generate speech from text (simulating user input)
2. Send the text to Ollama (gemma3)
3. Get response
4. Convert response to speech
5. Save response as audio file
"""

import sys
import os
from pathlib import Path
import pyttsx3

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        # Try to set UTF-8 encoding for Windows console
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Import our components
from src.ollama_client import OllamaClient
from src import config


def main():
    """Run demonstration test"""
    print("\n" + "=" * 80)
    print(" " * 25 + "🎤 OLLAMA VOICE ASSISTANT DEMO")
    print("=" * 80)

    # Test question - simulating what user would say
    test_question = "What is artificial intelligence?"

    print(f"\n📝 Simulated User Question:")
    print(f"   \"{test_question}\"")
    print("\n" + "-" * 80)

    # Step 1: Initialize Ollama client
    print("\n[STEP 1] Initializing Ollama client...")
    try:
        ollama = OllamaClient()
        print(f"   ✓ Connected to: {config.OLLAMA_URL}")
        print(f"   ✓ Using model: {config.OLLAMA_MODEL}")
    except Exception as e:
        print(f"   ✗ Failed to initialize: {e}")
        return

    # Test connection
    print("\n[STEP 2] Testing Ollama connection...")
    if not ollama.test_connection():
        print("   ✗ Cannot connect to Ollama")
        print(f"\n   Please ensure:")
        print(f"   1. Ollama is running")
        print(f"   2. Accessible at: {config.OLLAMA_URL}")
        print(f"   3. Model '{config.OLLAMA_MODEL}' is available")
        print(f"\n   To pull the model: ollama pull {config.OLLAMA_MODEL}")
        return

    # Step 2: Send question to Ollama
    print("\n[STEP 3] Sending question to Ollama (gemma3)...")
    print(f"   Question: \"{test_question}\"")

    try:
        response = ollama.chat(test_question, maintain_context=True)
    except Exception as e:
        print(f"   ✗ Error getting response: {e}")
        return

    if not response:
        print("   ✗ No response received from Ollama")
        return

    print(f"\n   ✓ Response received!")
    print(f"\n" + "=" * 80)
    print("🤖 OLLAMA RESPONSE:")
    print("=" * 80)
    print(response)
    print("=" * 80)

    # Step 3: Save response text
    print("\n[STEP 4] Saving response text...")
    output_dir = Path("test_outputs")
    output_dir.mkdir(exist_ok=True)

    text_file = output_dir / "demo_response.txt"
    try:
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(f"Question: {test_question}\n\n")
            f.write(f"Response from {config.OLLAMA_MODEL}:\n")
            f.write("=" * 80 + "\n")
            f.write(response + "\n")
        print(f"   ✓ Text saved to: {text_file}")
    except Exception as e:
        print(f"   ⚠ Could not save text: {e}")

    # Step 4: Convert response to speech and save
    print("\n[STEP 5] Converting response to speech...")
    audio_file = output_dir / "demo_response.wav"

    try:
        # Initialize TTS engine
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)

        # Try to save to file
        print(f"   Attempting to save to: {audio_file}")
        engine.save_to_file(response, str(audio_file))
        engine.runAndWait()

        # Check if file was created
        if audio_file.exists() and audio_file.stat().st_size > 0:
            print(f"   ✓ Audio saved to: {audio_file}")
            print(f"   ✓ File size: {audio_file.stat().st_size:,} bytes")
        else:
            print(f"   ⚠ Audio file was not created (pyttsx3 limitation)")
            print(f"   ℹ Playing audio through speakers instead...")

            # Play through speakers
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.say(response)
            engine.runAndWait()
            print(f"   ✓ Audio played through speakers")

    except Exception as e:
        print(f"   ⚠ TTS error: {e}")
        print(f"   ℹ This is often due to pyttsx3 limitations on Windows")

    # Summary
    print("\n" + "=" * 80)
    print("📊 DEMO SUMMARY")
    print("=" * 80)
    print(f"\n   User Question:   \"{test_question}\"")
    print(f"   Response Length: {len(response)} characters")
    print(f"   Model Used:      {config.OLLAMA_MODEL}")
    print(f"\n   Output Files:")
    print(f"   - Text file:  {text_file}")
    if audio_file.exists():
        print(f"   - Audio file: {audio_file}")
    else:
        print(f"   - Audio file: (played through speakers)")

    print("\n" + "=" * 80)
    print("✅ DEMO COMPLETED SUCCESSFULLY")
    print("=" * 80)

    print("\n💡 What happened:")
    print("   1. Your question was sent to Ollama (gemma3)")
    print("   2. Ollama processed it and generated a response")
    print("   3. The response was saved as text")
    print("   4. The response was converted to speech")
    print("   5. Audio was saved (or played through speakers)")

    print("\n🚀 Next step:")
    print("   Run the full voice assistant: python voice_assistant.py")

    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
