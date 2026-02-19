"""
Test Script - List Available Ollama Models

This script shows all models available on your Ollama server
"""

import sys
from src.ollama_client import OllamaClient
from src import config

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


def main():
    """List available Ollama models"""
    print("=" * 70)
    print("🤖 AVAILABLE OLLAMA MODELS")
    print("=" * 70)

    print(f"\n🔍 Connecting to: {config.OLLAMA_URL}")

    # Fetch models
    models = OllamaClient.get_available_models()

    if not models:
        print("\n❌ Could not fetch models from server")
        print("\nPossible reasons:")
        print("  - Ollama server is not running")
        print("  - URL is incorrect in config.py")
        print("  - Network connection issue")
        return

    print(f"\n✅ Found {len(models)} model(s):\n")

    # Display models
    for idx, model in enumerate(models, 1):
        model_name = model['name']
        model_size = model.get('size', 0)

        # Convert size to readable format
        if model_size > 1e9:
            size_str = f"{model_size / 1e9:.1f} GB"
        elif model_size > 1e6:
            size_str = f"{model_size / 1e6:.1f} MB"
        else:
            size_str = f"{model_size} bytes"

        # Mark current model
        current_marker = " [CURRENT]" if model_name == config.OLLAMA_MODEL else ""

        print(f"  [{idx}] {model_name}{current_marker}")
        print(f"       Size: {size_str}")

        # Show modified date if available
        if 'modified_at' in model:
            print(f"       Modified: {model['modified_at']}")

        print()

    print("=" * 70)
    print(f"\nℹ️  Current configured model: {config.OLLAMA_MODEL}")
    print(f"   (Set in src/config.py)")
    print("=" * 70)


if __name__ == "__main__":
    main()
