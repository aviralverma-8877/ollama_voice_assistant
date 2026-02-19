"""
Simple Test Script

Tests the pipeline with a text question (bypassing STT complexity):
1. Send text question to Ollama
2. Get response
3. Convert response to speech
4. Save response audio as WAV file
"""

import sys
import os
import numpy as np
from pathlib import Path
import pyttsx3
import wave

# Import our components
from src.text_to_speech import TextToSpeech
from src.ollama_client import OllamaClient
from src import config


def save_speech_to_file_alternative(text, output_file, rate=150):
    """
    Save speech to file using pyttsx3's save_to_file method

    Args:
        text: Text to convert to speech
        output_file: Output WAV file path
        rate: Speech rate in words per minute
    """
    try:
        # Create a new engine instance for file saving
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)
        engine.setProperty('volume', 0.9)

        # Save to file
        engine.save_to_file(text, output_file)
        engine.runAndWait()

        # Check if file was created and has content
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            if file_size > 0:
                print(f"✓ Speech saved to: {output_file} ({file_size:,} bytes)")
                return True
            else:
                print(f"⚠ File created but empty: {output_file}")
                return False
        else:
            print(f"⚠ File was not created: {output_file}")
            return False

    except Exception as e:
        print(f"❌ Error saving speech to file: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run simple test"""
    print("=" * 70)
    print("🧪 SIMPLE PIPELINE TEST")
    print("=" * 70)

    # Create output directory
    output_dir = Path("test_outputs")
    output_dir.mkdir(exist_ok=True)

    # Test questions
    test_questions = [
        "What is the capital of France?",
        "Explain quantum computing in simple terms.",
        "Tell me a short joke."
    ]

    print("\n📝 Test Questions:")
    for i, q in enumerate(test_questions, 1):
        print(f"   {i}. {q}")

    # Step 1: Initialize components
    print("\n" + "-" * 70)
    print("STEP 1: Initialize Components")
    print("-" * 70)

    try:
        tts = TextToSpeech()
        ollama = OllamaClient()
        print("✓ Components initialized")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return False

    # Step 2: Test Ollama connection
    print("\n" + "-" * 70)
    print("STEP 2: Test Ollama Connection")
    print("-" * 70)

    if not ollama.test_connection():
        print("❌ Cannot proceed without Ollama connection")
        return False

    # Step 3: Process each question
    print("\n" + "-" * 70)
    print("STEP 3: Process Questions")
    print("-" * 70)

    results = []

    for i, question in enumerate(test_questions, 1):
        print(f"\n{'=' * 70}")
        print(f"Question {i}: {question}")
        print('=' * 70)

        try:
            # Send to Ollama
            print(f"\n📤 Sending to Ollama...")
            response = ollama.chat(question, maintain_context=True)

            if not response:
                print("❌ No response received")
                continue

            print(f"\n✓ Response received:")
            print(f"📥 {response}")
            print(f"   Length: {len(response)} characters")

            # Save response text
            text_file = output_dir / f"response_{i}_text.txt"
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(f"Question: {question}\n\n")
                f.write(f"Response:\n{response}\n")
            print(f"\n✓ Response text saved to: {text_file}")

            # Convert to speech and save
            print(f"\n🔊 Converting to speech...")
            audio_file = output_dir / f"response_{i}_audio.wav"

            # Try to save to file
            if save_speech_to_file_alternative(response, str(audio_file)):
                print(f"✓ Audio saved successfully")
            else:
                print(f"⚠ Could not save audio file")
                print(f"  Playing through speakers instead...")
                tts.speak(response)
                print(f"✓ Response played through speakers")

            results.append({
                'question': question,
                'response': response,
                'text_file': text_file,
                'audio_file': audio_file if audio_file.exists() else None
            })

        except Exception as e:
            print(f"\n❌ Error processing question: {e}")
            import traceback
            traceback.print_exc()
            continue

    # Clear context
    ollama.clear_context()

    # Step 4: Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)

    print(f"\n✓ Processed {len(results)} questions successfully")

    for i, result in enumerate(results, 1):
        print(f"\n  Question {i}: {result['question']}")
        print(f"    Response length: {len(result['response'])} chars")
        print(f"    Text file: {result['text_file']}")
        if result['audio_file']:
            print(f"    Audio file: {result['audio_file']}")
        else:
            print(f"    Audio file: (not saved)")

    print(f"\n  All output files in: {output_dir.absolute()}")

    print("\n" + "=" * 70)
    print("✅ TEST COMPLETED")
    print("=" * 70)

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
