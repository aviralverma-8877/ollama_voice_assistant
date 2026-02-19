"""
Speech-to-Text - Converts speech to text using Vosk
"""

import json
import os
from vosk import Model, KaldiRecognizer
import numpy as np
from . import config


class SpeechToText:
    """Handles speech-to-text conversion using Vosk"""

    def __init__(self, model_path: str = None):
        """
        Initialize Vosk speech recognition

        Args:
            model_path: Path to Vosk model directory
        """
        self.model_path = model_path or config.VOSK_MODEL_PATH

        # Check if model exists
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"\n❌ Vosk model not found at: {self.model_path}\n"
                f"Please download a model from: https://alphacephei.com/vosk/models\n"
                f"Recommended: vosk-model-small-en-us-0.15\n"
                f"Extract the model to: {self.model_path}"
            )

        print(f"\n🎤 Loading Vosk model from: {self.model_path}")
        self.model = Model(self.model_path)
        self.sample_rate = config.SAMPLE_RATE
        print(f"✓ Vosk model loaded successfully")

    def create_recognizer(self) -> KaldiRecognizer:
        """Create a new recognizer instance"""
        return KaldiRecognizer(self.model, self.sample_rate)

    def transcribe_audio(self, audio_data: np.ndarray) -> str:
        """
        Transcribe audio data to text

        Args:
            audio_data: Audio data as numpy array (int16)

        Returns:
            Transcribed text
        """
        recognizer = self.create_recognizer()

        # Convert numpy array to bytes
        if audio_data.dtype != np.int16:
            audio_data = (audio_data * 32767).astype(np.int16)

        audio_bytes = audio_data.tobytes()

        # Process audio
        recognizer.AcceptWaveform(audio_bytes)

        # Get result
        result = json.loads(recognizer.FinalResult())
        text = result.get('text', '').strip()

        return text

    def transcribe_stream(self, audio_chunk: bytes, recognizer: KaldiRecognizer) -> tuple[str, str]:
        """
        Transcribe audio stream chunk by chunk

        Args:
            audio_chunk: Audio chunk as bytes
            recognizer: KaldiRecognizer instance

        Returns:
            Tuple of (partial_text, final_text)
            - partial_text: Intermediate recognition result
            - final_text: Final result when speech segment ends
        """
        partial_text = ""
        final_text = ""

        if recognizer.AcceptWaveform(audio_chunk):
            # Final result (end of speech segment)
            result = json.loads(recognizer.Result())
            final_text = result.get('text', '').strip()
        else:
            # Partial result (ongoing speech)
            result = json.loads(recognizer.PartialResult())
            partial_text = result.get('partial', '').strip()

        return partial_text, final_text

    def listen_for_speech(self, audio_manager, timeout: float = 10.0, silence_threshold: float = 2.0) -> str:
        """
        Listen for speech and transcribe it

        Args:
            audio_manager: AudioManager instance for recording
            timeout: Maximum time to listen (seconds)
            silence_threshold: Time of silence before stopping (seconds)

        Returns:
            Transcribed text
        """
        recognizer = self.create_recognizer()
        transcribed_text = []
        last_speech_time = 0
        elapsed_time = 0
        chunk_duration = 0.25  # 250ms chunks

        print("🎤 Listening... (speak now)")

        def process_chunk(audio_chunk):
            nonlocal last_speech_time, elapsed_time, transcribed_text

            # Convert to bytes
            audio_bytes = audio_chunk.tobytes()

            # Process with Vosk
            partial_text, final_text = self.transcribe_stream(audio_bytes, recognizer)

            # Update elapsed time
            elapsed_time += chunk_duration

            if partial_text:
                # Speech detected
                last_speech_time = elapsed_time
                print(f"   Hearing: {partial_text}", end='\r')

            if final_text:
                # Complete phrase recognized
                transcribed_text.append(final_text)
                print(f"\n   Recognized: {final_text}")
                last_speech_time = elapsed_time

            # Check stop conditions
            silence_duration = elapsed_time - last_speech_time

            # Stop if timeout reached
            if elapsed_time >= timeout:
                print("\n⏱ Timeout reached")
                return False

            # Stop if silence threshold reached (but only if we've heard something)
            if transcribed_text and silence_duration >= silence_threshold:
                print("\n🔇 Silence detected, processing...")
                return False

            return True

        # Record stream with callback
        audio_manager.record_stream(process_chunk, chunk_duration=chunk_duration)

        # Combine all transcribed text
        full_text = ' '.join(transcribed_text).strip()

        return full_text
