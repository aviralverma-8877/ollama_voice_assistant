"""
Ollama Client - Handles communication with Ollama API
"""

import requests
from typing import List, Dict, Optional
from . import config


class OllamaClient:
    """Client for interacting with Ollama API"""

    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = base_url or config.OLLAMA_URL
        self.model = model or config.OLLAMA_MODEL
        self.conversation_history: List[Dict[str, str]] = []
        self.max_context = config.MAX_CONTEXT_MESSAGES

        # Ensure URL doesn't end with slash
        self.base_url = self.base_url.rstrip('/')

        print(f"\n🤖 Ollama Client initialized")
        print(f"   URL: {self.base_url}")
        print(f"   Model: {self.model}")

    def chat(self, user_message: str, maintain_context: bool = True) -> str:
        """
        Send a message to Ollama and get a response

        Args:
            user_message: The user's message/question
            maintain_context: Whether to include conversation history

        Returns:
            The assistant's response
        """
        try:
            # Add user message to history
            if maintain_context:
                self.conversation_history.append({
                    "role": "user",
                    "content": user_message
                })

                # Trim history if too long
                if len(self.conversation_history) > self.max_context * 2:  # *2 because user+assistant pairs
                    self.conversation_history = self.conversation_history[-self.max_context * 2:]

                messages = self.conversation_history
            else:
                messages = [{"role": "user", "content": user_message}]

            # Make request to Ollama
            url = f"{self.base_url}/api/chat"
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False
            }

            print(f"📤 Sending request to Ollama...")
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()

            # Extract response
            result = response.json()
            assistant_message = result.get("message", {}).get("content", "")

            # Add assistant response to history
            if maintain_context and assistant_message:
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_message
                })

            print(f"📥 Received response from Ollama")
            return assistant_message

        except requests.exceptions.Timeout:
            error_msg = "Request to Ollama timed out. Please try again."
            print(f"❌ {error_msg}")
            return error_msg

        except requests.exceptions.ConnectionError:
            error_msg = f"Could not connect to Ollama at {self.base_url}. Please check if Ollama is running."
            print(f"❌ {error_msg}")
            return error_msg

        except requests.exceptions.HTTPError as e:
            error_msg = f"Ollama API error: {e}"
            print(f"❌ {error_msg}")
            return f"Sorry, there was an error communicating with the assistant."

        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            print(f"❌ {error_msg}")
            return "Sorry, an unexpected error occurred."

    def clear_context(self):
        """Clear the conversation history"""
        self.conversation_history = []
        print("🔄 Conversation context cleared")

    def get_context_size(self) -> int:
        """Get the number of messages in the conversation history"""
        return len(self.conversation_history)

    def test_connection(self) -> bool:
        """Test connection to Ollama server"""
        try:
            url = f"{self.base_url}/api/tags"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            print(f"✓ Successfully connected to Ollama at {self.base_url}")

            # List available models
            models = response.json().get("models", [])
            if models:
                print(f"  Available models: {', '.join([m['name'] for m in models])}")

                # Check if configured model is available
                model_names = [m['name'] for m in models]
                if self.model not in model_names:
                    print(f"  ⚠ Warning: Model '{self.model}' not found in available models")
                    print(f"  You may need to pull it with: ollama pull {self.model}")

            return True

        except Exception as e:
            print(f"✗ Failed to connect to Ollama at {self.base_url}: {e}")
            return False
