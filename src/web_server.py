"""
Web Server - Flask server for web-based voice assistant interface
"""

import os
import io
import tempfile
import wave
import socket
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import numpy as np

from .speech_to_text import SpeechToText
from .text_to_speech import TextToSpeech
from .ollama_client import OllamaClient
from . import config


class WebServer:
    """Web server for voice assistant"""

    def __init__(self, model: str = None, host: str = "0.0.0.0", port: int = 5000):
        """
        Initialize web server

        Args:
            model: Ollama model to use
            host: Host to bind to (default: 0.0.0.0 for network access)
            port: Port to listen on
        """
        self.app = Flask(__name__,
                        static_folder='../static',
                        template_folder='../templates')
        CORS(self.app)  # Enable CORS for browser requests

        self.host = host
        self.port = port

        # Initialize components
        print("\n🌐 Initializing web server components...")
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self.ollama = OllamaClient(model=model)

        # Conversation context
        self.conversation_history = []

        # Register routes
        self._register_routes()

        print(f"✓ Web server initialized")

    def _register_routes(self):
        """Register Flask routes"""

        @self.app.route('/')
        def index():
            """Serve the main page"""
            return render_template('index.html', wake_word=config.WAKE_WORD)

        @self.app.route('/api/process_audio', methods=['POST'])
        def process_audio():
            """
            Process audio from the browser
            Expects: WAV audio file
            Returns: JSON with transcribed text and response
            """
            try:
                # Get audio file from request
                if 'audio' not in request.files:
                    return jsonify({'error': 'No audio file provided'}), 400

                audio_file = request.files['audio']

                # Read audio data
                audio_bytes = audio_file.read()

                # Parse WAV file
                with io.BytesIO(audio_bytes) as wav_io:
                    with wave.open(wav_io, 'rb') as wav_file:
                        # Get audio parameters
                        channels = wav_file.getnchannels()
                        sample_width = wav_file.getsampwidth()
                        framerate = wav_file.getframerate()

                        # Read audio frames
                        audio_data = wav_file.readframes(wav_file.getnframes())

                        # Convert to numpy array
                        if sample_width == 2:  # 16-bit
                            audio_array = np.frombuffer(audio_data, dtype=np.int16)
                        else:
                            return jsonify({'error': f'Unsupported sample width: {sample_width}'}), 400

                        # Convert stereo to mono if needed
                        if channels == 2:
                            audio_array = audio_array.reshape(-1, 2).mean(axis=1).astype(np.int16)

                print(f"\n📥 Received audio: {len(audio_array)} samples at {framerate} Hz")

                # Transcribe audio
                print("🔄 Transcribing audio...")
                text = self.stt.transcribe_audio(audio_array, source_sample_rate=framerate)

                if not text:
                    return jsonify({
                        'success': False,
                        'error': 'No speech detected. Please speak louder or check your microphone.'
                    }), 200

                print(f"✓ Transcribed: \"{text}\"")

                # Check if wake word is present (optional for web interface)
                # In web mode, we can skip wake word requirement or make it optional
                # For now, let's process all audio

                # Get response from Ollama
                print("🤖 Getting response from Ollama...")
                self.conversation_history.append({"role": "user", "content": text})

                response = self.ollama.chat(self.conversation_history)

                if response:
                    self.conversation_history.append({"role": "assistant", "content": response})
                    print(f"✓ Response: \"{response[:100]}...\"")
                else:
                    response = "I'm sorry, I couldn't generate a response."

                # Generate audio response
                print("🔊 Generating audio response...")
                # Save TTS to temporary file
                temp_audio_path = os.path.join(tempfile.gettempdir(), 'tts_response.wav')

                # Use pyttsx3 to save to file
                self.tts.engine.save_to_file(response, temp_audio_path)
                self.tts.engine.runAndWait()

                # Read the generated audio file
                with open(temp_audio_path, 'rb') as f:
                    audio_response = f.read()

                # Clean up temp file
                try:
                    os.remove(temp_audio_path)
                except:
                    pass

                return jsonify({
                    'success': True,
                    'transcribed_text': text,
                    'response_text': response,
                    'has_audio': True
                })

            except Exception as e:
                print(f"❌ Error processing audio: {e}")
                import traceback
                traceback.print_exc()
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/get_response_audio', methods=['POST'])
        def get_response_audio():
            """
            Generate and return audio for a text response
            """
            try:
                data = request.get_json()
                text = data.get('text', '')

                if not text:
                    return jsonify({'error': 'No text provided'}), 400

                print(f"🔊 Generating audio for: \"{text[:50]}...\"")

                # Generate audio response
                temp_audio_path = os.path.join(tempfile.gettempdir(), 'tts_response.wav')

                # Use pyttsx3 to save to file
                self.tts.engine.save_to_file(text, temp_audio_path)
                self.tts.engine.runAndWait()

                # Return the audio file
                return send_file(
                    temp_audio_path,
                    mimetype='audio/wav',
                    as_attachment=False,
                    download_name='response.wav'
                )

            except Exception as e:
                print(f"❌ Error generating audio: {e}")
                import traceback
                traceback.print_exc()
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/clear_history', methods=['POST'])
        def clear_history():
            """Clear conversation history"""
            self.conversation_history = []
            return jsonify({'success': True, 'message': 'Conversation history cleared'})

        @self.app.route('/api/status', methods=['GET'])
        def status():
            """Get server status"""
            return jsonify({
                'status': 'running',
                'wake_word': config.WAKE_WORD,
                'model': self.ollama.model,
                'messages_in_history': len(self.conversation_history)
            })

    def run(self):
        """Start the web server"""
        # Get local IP address
        local_ip = "localhost"
        try:
            # Get the local IP address
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except:
            pass

        print("\n" + "=" * 70)
        print("🌐 VOICE ASSISTANT WEB SERVER")
        print("=" * 70)
        print(f"\n🔗 Access the web interface from:")

        if self.host == "0.0.0.0":
            print(f"   • Local:   http://localhost:{self.port}")
            print(f"   • Network: http://{local_ip}:{self.port}")
            print(f"\n💡 Share the network URL with other devices on your local network")
        else:
            print(f"   http://{self.host}:{self.port}")

        print(f"\n📋 Wake word: '{config.WAKE_WORD}' (optional in web mode)")
        print(f"🤖 Using model: {self.ollama.model}")
        print("\n⚠  Press Ctrl+C to stop the server")
        print("=" * 70 + "\n")

        try:
            self.app.run(host=self.host, port=self.port, debug=False)
        except KeyboardInterrupt:
            print("\n\n⏹  Server stopped by user")


def start_web_server(model: str = None, host: str = "0.0.0.0", port: int = 5000):
    """
    Start the web server

    Args:
        model: Ollama model to use
        host: Host to bind to (default: 0.0.0.0 for network access)
        port: Port to listen on (default: 5000)
    """
    server = WebServer(model=model, host=host, port=port)
    server.run()
