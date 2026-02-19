"""
Test Web Server Functionality
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def test_imports():
    """Test that all required modules can be imported"""
    print("\n" + "=" * 70)
    print("🧪 TESTING WEB SERVER IMPORTS")
    print("=" * 70)

    try:
        print("\n✓ Testing Flask import...")
        from flask import Flask
        print("  ✅ Flask imported successfully")

        print("\n✓ Testing flask-cors import...")
        from flask_cors import CORS
        print("  ✅ flask-cors imported successfully")

        print("\n✓ Testing web_server module import...")
        from src.web_server import WebServer, start_web_server
        print("  ✅ web_server module imported successfully")

        print("\n✓ Testing other dependencies...")
        from src.speech_to_text import SpeechToText
        from src.text_to_speech import TextToSpeech
        from src.ollama_client import OllamaClient
        print("  ✅ All dependencies imported successfully")

        return True

    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_web_server_initialization():
    """Test that web server can be initialized"""
    print("\n" + "=" * 70)
    print("🧪 TESTING WEB SERVER INITIALIZATION")
    print("=" * 70)

    try:
        print("\n✓ Initializing WebServer...")
        from src.web_server import WebServer

        # Initialize without starting (to avoid blocking)
        server = WebServer(model="gemma3:4b", host="127.0.0.1", port=5000)
        print("  ✅ WebServer initialized successfully")

        # Check attributes
        print("\n✓ Checking server attributes...")
        assert hasattr(server, 'app'), "Server should have 'app' attribute"
        assert hasattr(server, 'stt'), "Server should have 'stt' attribute"
        assert hasattr(server, 'tts'), "Server should have 'tts' attribute"
        assert hasattr(server, 'ollama'), "Server should have 'ollama' attribute"
        assert hasattr(server, 'conversation_history'), "Server should have 'conversation_history' attribute"
        print("  ✅ All attributes present")

        # Check routes
        print("\n✓ Checking registered routes...")
        routes = [rule.rule for rule in server.app.url_map.iter_rules()]
        expected_routes = ['/', '/api/process_audio', '/api/get_response_audio',
                          '/api/clear_history', '/api/status']
        for route in expected_routes:
            assert route in routes, f"Route {route} should be registered"
        print(f"  ✅ All {len(expected_routes)} routes registered")

        return True

    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_template_exists():
    """Test that HTML template exists"""
    print("\n" + "=" * 70)
    print("🧪 TESTING TEMPLATE FILES")
    print("=" * 70)

    try:
        print("\n✓ Checking for templates/index.html...")
        template_path = "templates/index.html"

        if not os.path.exists(template_path):
            print(f"  ❌ Template not found at: {template_path}")
            return False

        print(f"  ✅ Template found at: {template_path}")

        # Check file size
        file_size = os.path.getsize(template_path)
        print(f"  ℹ️  Template size: {file_size:,} bytes")

        if file_size < 100:
            print(f"  ⚠️  Template seems too small")
            return False

        print("  ✅ Template size looks good")

        return True

    except Exception as e:
        print(f"\n❌ Template check failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_static_directory():
    """Test that static directory exists"""
    print("\n" + "=" * 70)
    print("🧪 TESTING STATIC DIRECTORY")
    print("=" * 70)

    try:
        print("\n✓ Checking for static/ directory...")

        if not os.path.exists("static"):
            print("  ⚠️  Static directory not found (optional)")
            os.makedirs("static", exist_ok=True)
            print("  ✅ Created static directory")
        else:
            print("  ✅ Static directory exists")

        return True

    except Exception as e:
        print(f"\n❌ Static directory check failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("🧪 WEB SERVER TEST SUITE")
    print("=" * 70)
    print("\nThis will test web server components without starting the server.")

    results = []

    # Test 1: Imports
    results.append(("Imports", test_imports()))

    # Test 2: Initialization
    results.append(("Initialization", test_web_server_initialization()))

    # Test 3: Template
    results.append(("Template", test_template_exists()))

    # Test 4: Static Directory
    results.append(("Static Directory", test_static_directory()))

    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")

    print(f"\n  Result: {passed}/{total} tests passed")

    if passed == total:
        print("\n✅ All tests passed! Web server is ready to use.")
        print("\nTo start the web server:")
        print("  1. Run: python main.py")
        print("  2. Select: [2] Web Mode")
        print("  3. Open: http://127.0.0.1:5000")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")

    print("=" * 70)

    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
