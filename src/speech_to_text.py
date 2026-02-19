"""
Speech-to-Text - Converts speech to text using Vosk
"""

import json
import os
from vosk import Model, KaldiRecognizer
import numpy as np
from scipy import signal
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

    def transcribe_audio(self, audio_data: np.ndarray, source_sample_rate: int = None) -> str:
        """
        Transcribe audio data to text

        Args:
            audio_data: Audio data as numpy array (int16 or float32)
            source_sample_rate: Original sample rate of the audio (if None, assumes config.SAMPLE_RATE)

        Returns:
            Transcribed text
        """
        recognizer = self.create_recognizer()

        # Debug info
        print(f"   Audio shape: {audio_data.shape}, dtype: {audio_data.dtype}")
        print(f"   Audio range: min={np.min(audio_data):.4f}, max={np.max(audio_data):.4f}")

        # Convert stereo to mono if needed
        if len(audio_data.shape) > 1 and audio_data.shape[1] > 1:
            print(f"   Converting stereo to mono...")
            # Average the channels
            audio_data = np.mean(audio_data, axis=1)

        # Ensure audio is 1D array
        if len(audio_data.shape) > 1:
            print(f"   Flattening audio array from shape {audio_data.shape}")
            audio_data = audio_data.flatten()

        # Determine source sample rate
        if source_sample_rate is None:
            source_sample_rate = self.sample_rate

        # Resample if needed
        if source_sample_rate != self.sample_rate:
            print(f"   Resampling from {source_sample_rate} Hz to {self.sample_rate} Hz...")
            # Convert to float for resampling
            if audio_data.dtype == np.int16:
                audio_float = audio_data.astype(np.float32) / 32767.0
            else:
                audio_float = audio_data.astype(np.float32)

            # Calculate number of samples after resampling
            num_samples = int(len(audio_float) * self.sample_rate / source_sample_rate)

            # Resample using scipy
            audio_resampled = signal.resample(audio_float, num_samples)

            # Convert back to int16
            audio_data = (audio_resampled * 32767).astype(np.int16)
        else:
            # Convert numpy array to int16 if needed
            if audio_data.dtype != np.int16:
                audio_data = (audio_data * 32767).astype(np.int16)

        # Apply automatic gain control if signal is too weak
        max_amplitude = np.max(np.abs(audio_data))
        if max_amplitude > 0:
            target_amplitude = 10000  # Target level (about 30% of max)
            if max_amplitude < 3000:  # If signal is weak (< 10% of max)
                gain = min(target_amplitude / max_amplitude, 10.0)  # Cap gain at 10x
                print(f"   ⚠ Low audio level detected ({max_amplitude}). Applying {gain:.1f}x gain...")
                audio_data = np.clip(audio_data * gain, -32767, 32767).astype(np.int16)
                print(f"   New max amplitude: {np.max(np.abs(audio_data))}")

        # Final debug info
        print(f"   Final audio shape: {audio_data.shape}, dtype: {audio_data.dtype}")
        print(f"   Processing {len(audio_data)} samples...")

        audio_bytes = audio_data.tobytes()

        # Process audio
        recognizer.AcceptWaveform(audio_bytes)

        # Get result
        result = json.loads(recognizer.FinalResult())
        text = result.get('text', '').strip()

        print(f"   Vosk result: {result}")

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
