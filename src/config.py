# Configuration for Ollama Voice Assistant

# Ollama Configuration
OLLAMA_URL = "https://home.iot-connect.in"
OLLAMA_MODEL = "gemma3:4b"  # Change to your preferred model (e.g., llama3, mistral, etc.)
PROMPT_MODEL_SELECTION = True  # Prompt user to select Ollama model on startup

# Audio Configuration
SAMPLE_RATE = 16000  # Vosk works best with 16kHz
CHANNELS = 1  # Mono audio
CHUNK_SIZE = 4000  # Audio chunk size for processing
PROMPT_DEVICE_SELECTION = True  # Prompt user to select audio devices on startup
PROMPT_DEVICE_TEST = True  # Prompt user to test audio devices after selection

# Wake Word Configuration
WAKE_WORD = "hello lamma"
WAKE_WORD_THRESHOLD = 0.7  # Confidence threshold for wake word detection

# Vosk Model Path (download required)
# Download small model from: https://alphacephei.com/vosk/models
# Recommended: vosk-model-small-en-us-0.15
VOSK_MODEL_PATH = "models/vosk-model-small-en-us-0.15"

# Bluetooth Configuration (optional - set to None to use default audio device)
BLUETOOTH_DEVICE_NAME = None  # e.g., "JBL Flip 5" or None for default device
BLUETOOTH_MAC_ADDRESS = None  # e.g., "XX:XX:XX:XX:XX:XX" or None
# Note: 100ms delay is automatically applied before all audio I/O operations
# to accommodate Bluetooth device latency

# Session Configuration
SESSION_TIMEOUT = 300  # Seconds of inactivity before ending session (5 minutes)
MAX_CONTEXT_MESSAGES = 10  # Maximum conversation history to maintain

# Beep Sound Configuration
BEEP_FREQUENCY = 1000  # Hz
BEEP_DURATION = 0.2  # Seconds
