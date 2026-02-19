"""
Wake Word Detector - Detects wake word using Vosk
"""

import json
from vosk import KaldiRecognizer
from .speech_to_text import SpeechToText
from . import config


class WakeWordDetector:
    """Detects wake word from audio stream"""

    def __init__(self, wake_word: str = None, threshold: float = None):
        """
        Initialize wake word detector

        Args:
            wake_word: The wake word to detect (e.g., "hello lamma")
            threshold: Confidence threshold (not used with Vosk keyword matching)
        """
        self.wake_word = (wake_word or config.WAKE_WORD).lower().strip()
        self.threshold = threshold or config.WAKE_WORD_THRESHOLD

        # Initialize speech recognition
        self.stt = SpeechToText()

        print(f"\n🎯 Wake Word Detector initialized")
        print(f"   Wake word: '{self.wake_word}'")

    def listen_for_wake_word(self, audio_manager) -> bool:
        """
        Listen continuously for the wake word

        Args:
            audio_manager: AudioManager instance

        Returns:
            True when wake word is detected
        """
        recognizer = self.stt.create_recognizer()
        chunk_duration = 0.5  # 500ms chunks for wake word detection

        print(f"\n👂 Listening for wake word: '{self.wake_word}'...")
        print("   (Press Ctrl+C to exit)")

        wake_word_detected = False

        def process_chunk(audio_chunk):
            nonlocal wake_word_detected

            # Convert to bytes
            audio_bytes = audio_chunk.tobytes()

            # Process with Vosk
            if recognizer.AcceptWaveform(audio_bytes):
                # Final result
                result = json.loads(recognizer.Result())
                text = result.get('text', '').lower().strip()

                if text:
                    # Check if wake word is in the recognized text
                    if self._matches_wake_word(text):
                        print(f"\n✓ Wake word detected: '{text}'")
                        wake_word_detected = True
                        return False  # Stop listening
            else:
                # Partial result - also check for wake word
                result = json.loads(recognizer.PartialResult())
                partial = result.get('partial', '').lower().strip()

                if partial and self._matches_wake_word(partial):
                    print(f"\n✓ Wake word detected: '{partial}'")
                    wake_word_detected = True
                    return False  # Stop listening

            return True  # Continue listening

        try:
            audio_manager.record_stream(process_chunk, chunk_duration=chunk_duration)
        except KeyboardInterrupt:
            print("\n\nWake word detection stopped by user")
            return False

        return wake_word_detected

    def _matches_wake_word(self, text: str) -> bool:
        """
        Check if text contains the wake word

        Args:
            text: Recognized text (already lowercased)

        Returns:
            True if wake word is found in text
        """
        # Exact match
        if text == self.wake_word:
            return True

        # Wake word is contained in the text
        if self.wake_word in text:
            return True

        # Check for similar matches (handle slight variations)
        # For "hello lamma", also accept "hello llama", "hello lama", etc.
        wake_word_parts = self.wake_word.split()

        # All parts must be present
        if all(part in text for part in wake_word_parts):
            return True

        # Check for fuzzy match (optional - more lenient)
        # This checks if the words appear in order
        text_words = text.split()
        wake_word_words = wake_word_parts

        if len(text_words) >= len(wake_word_words):
            for i in range(len(text_words) - len(wake_word_words) + 1):
                # Check if wake word words appear consecutively
                match = True
                for j, wake_word in enumerate(wake_word_words):
                    if not self._words_similar(text_words[i + j], wake_word):
                        match = False
                        break
                if match:
                    return True

        return False

    def _words_similar(self, word1: str, word2: str, max_distance: int = 2) -> bool:
        """
        Check if two words are similar (Levenshtein distance)

        Args:
            word1: First word
            word2: Second word
            max_distance: Maximum edit distance to consider similar

        Returns:
            True if words are similar
        """
        # Exact match
        if word1 == word2:
            return True

        # Simple length check
        if abs(len(word1) - len(word2)) > max_distance:
            return False

        # Calculate Levenshtein distance
        distance = self._levenshtein_distance(word1, word2)

        return distance <= max_distance

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """
        Calculate Levenshtein distance between two strings

        Args:
            s1: First string
            s2: Second string

        Returns:
            Edit distance
        """
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)

        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                # Cost of insertions, deletions, or substitutions
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]
