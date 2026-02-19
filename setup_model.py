"""
Setup script to download and extract Vosk model
"""

import os
import sys
import urllib.request
import zipfile
from pathlib import Path


def download_file(url, destination):
    """Download file with progress bar"""
    print(f"Downloading from {url}...")

    def reporthook(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = min(downloaded * 100 / total_size, 100)
            sys.stdout.write(f"\r  Progress: {percent:.1f}% ({downloaded // (1024*1024)}MB / {total_size // (1024*1024)}MB)")
            sys.stdout.flush()

    urllib.request.urlretrieve(url, destination, reporthook)
    print("\n✓ Download complete")


def extract_zip(zip_path, extract_to):
    """Extract zip file"""
    print(f"Extracting to {extract_to}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print("✓ Extraction complete")


def main():
    """Download and setup Vosk model"""
    print("=" * 60)
    print("VOSK MODEL SETUP")
    print("=" * 60)

    # Model details
    model_name = "vosk-model-small-en-us-0.15"
    model_url = f"https://alphacephei.com/vosk/models/{model_name}.zip"
    models_dir = Path("models")
    model_path = models_dir / model_name
    zip_path = models_dir / f"{model_name}.zip"

    # Check if model already exists
    if model_path.exists():
        print(f"\n✓ Model already exists at: {model_path}")
        print("  No download needed.")
        return

    # Create models directory
    models_dir.mkdir(exist_ok=True)

    try:
        # Download model
        print(f"\nDownloading Vosk model: {model_name}")
        print("  Size: ~39 MB")
        print()
        download_file(model_url, zip_path)

        # Extract model
        print()
        extract_zip(zip_path, models_dir)

        # Remove zip file
        print("\nCleaning up...")
        zip_path.unlink()

        print("\n" + "=" * 60)
        print("✓ SETUP COMPLETE!")
        print("=" * 60)
        print(f"\nModel installed at: {model_path}")
        print("\nYou can now run: python voice_assistant.py")

    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        print("\nYou can manually download the model from:")
        print("  https://alphacephei.com/vosk/models")
        print(f"\nExtract to: {model_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
