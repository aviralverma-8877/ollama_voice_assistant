# Web Mode Guide

The voice assistant now supports a **Web Mode** that allows you to interact with it through a beautiful web interface instead of the command line!

## 🌐 What is Web Mode?

Web Mode launches a local web server that hosts a browser-based interface for the voice assistant. Instead of using your terminal and microphone directly, you can:

- Open a webpage in your browser
- Click a button to record your voice
- See the transcribed text
- Read the assistant's response
- Listen to the audio response

This is perfect for:
- Users who prefer a visual interface
- Remote access scenarios
- Better conversation history viewing
- Multi-user access (everyone on the same network can use it)

## 🚀 How to Use Web Mode

### Step 1: Start the Assistant

```bash
python main.py
```

### Step 2: Select Mode

When prompted, choose option **[2] Web Mode**:

```
🎙️  VOICE ASSISTANT - MODE SELECTION

How would you like to use the voice assistant?
  [1] CLI Mode  - Use microphone directly in terminal
  [2] Web Mode  - Launch web server with browser interface

Your choice [1/2]: 2
```

### Step 3: Configure Server (Optional)

You can use the default settings or customize:

```
Default settings:
  Host: 127.0.0.1
  Port: 5000

Use custom settings?
  [1] Yes - Let me configure
  [2] No  - Use defaults
```

**Defaults work great for most users!**

### Step 4: Open Your Browser

Once the server starts, you'll see:

```
🌐 VOICE ASSISTANT WEB SERVER

🔗 Open your browser and navigate to:
   http://127.0.0.1:5000

📋 Wake word: 'computer' (optional in web mode)
🤖 Using model: gemma3:4b

⚠  Press Ctrl+C to stop the server
```

**Click the link** or open your browser and go to: `http://127.0.0.1:5000`

### Step 5: Use the Web Interface

1. **Click the microphone button** 🎤 (it will turn red when recording)
2. **Speak your question** (no wake word needed!)
3. **Click again to stop** recording
4. Watch as:
   - Your speech is transcribed
   - The assistant generates a response
   - Audio response plays automatically

## ✨ Features

### Beautiful Interface
- Modern, gradient design
- Smooth animations
- Mobile-responsive

### Voice Recording
- Click-to-record (no wake word needed)
- Visual recording indicator
- Automatic audio processing

### Conversation History
- See all your past messages
- User messages in blue
- Assistant responses in purple
- Auto-scroll to latest message

### Audio Playback
- Automatic audio response playback
- Audio player controls for each response
- Can replay responses anytime

### Status Messages
- Real-time status updates
- Clear error messages
- Processing indicators

### Actions
- **Clear History** - Start a fresh conversation
- **Check Status** - See server info and model being used

## 🔧 Configuration

### Change Default Port

If port 5000 is already in use, you can change it:

```python
# When prompted, select "Yes - Let me configure"
# Then enter your desired port (e.g., 8080, 3000, etc.)
```

### Allow Remote Access

To access from other devices on your network:

```python
# When prompted, enter:
# Host: 0.0.0.0
# Port: 5000 (or any port you prefer)
```

Then access from other devices using: `http://YOUR_COMPUTER_IP:5000`

### Change Model

When starting in web mode, you'll still be prompted to select an Ollama model if `PROMPT_MODEL_SELECTION = True` in `src/config.py`.

## 🆚 CLI Mode vs Web Mode

| Feature | CLI Mode | Web Mode |
|---------|----------|----------|
| **Interface** | Terminal | Browser |
| **Wake Word** | Required ("computer") | Not needed |
| **Audio Input** | Direct microphone | Button-click recording |
| **Conversation History** | No visual history | Full visual history |
| **Audio Playback** | Automatic speaker | Audio player controls |
| **Multi-user** | Single user | Multiple users can access |
| **Remote Access** | Local only | Can be network-accessible |
| **Microphone Setup** | May need volume adjustments | Browser handles it |

## 🛠️ Troubleshooting

### Port Already in Use

If you see: `Address already in use`

**Solution:** Choose a different port when configuring, or stop the other program using port 5000.

### Microphone Not Working

**Solution:** Check browser permissions:
1. Click the lock icon in the address bar
2. Allow microphone access
3. Refresh the page

### "No speech detected"

**Solutions:**
1. Speak louder and closer to the microphone
2. Check browser microphone settings
3. Try a different browser (Chrome/Edge work best)
4. Ensure browser has microphone permissions

### Server Won't Start

**Solution:** Make sure Flask is installed:

```bash
pip install -r requirements.txt
```

### Can't Access from Another Device

**Solutions:**
1. Make sure you configured `host: 0.0.0.0`
2. Check your firewall settings
3. Ensure both devices are on the same network
4. Use your computer's IP address, not 127.0.0.1

## 🔒 Security Notes

- **Local Network Only**: By default, the server only accepts connections from your computer (127.0.0.1)
- **No Authentication**: Web mode doesn't have password protection
- **Don't Expose to Internet**: This is meant for local/trusted network use only
- **Conversation History**: Stored in memory only, cleared when server restarts

## 💡 Tips

1. **No Wake Word Needed**: Unlike CLI mode, you don't need to say "computer" first - just click and speak!

2. **Better for Testing**: Web mode is great when testing speech recognition since you can see exactly what was transcribed.

3. **Multiple Conversations**: Open multiple browser tabs to see different conversation threads.

4. **Mobile Access**: If you set `host: 0.0.0.0`, you can access from your phone browser on the same WiFi network.

5. **Clear History**: Click "Clear History" to start a fresh conversation without restarting the server.

## 📱 Mobile Usage

Yes, you can use it on your phone!

1. Start the server with `host: 0.0.0.0`
2. Find your computer's IP address:
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig`
3. Open your phone's browser
4. Go to: `http://YOUR_COMPUTER_IP:5000`
5. Tap the microphone to speak

## 🎯 When to Use Each Mode

**Use CLI Mode when:**
- You prefer keyboard and terminal interfaces
- You want hands-free operation with wake words
- You're comfortable with command-line tools
- You want the assistant always listening

**Use Web Mode when:**
- You prefer visual interfaces
- You want to see conversation history
- You're testing or debugging speech recognition
- You want to access from multiple devices
- You prefer button-click recording over always-listening

## 📦 Installation

Web mode requires Flask, which is included in `requirements.txt`:

```bash
pip install -r requirements.txt
```

This installs:
- `Flask==3.0.0` - Web framework
- `flask-cors==4.0.0` - Cross-origin support

## 🚀 Quick Start Example

```bash
# 1. Install requirements
pip install -r requirements.txt

# 2. Start the assistant
python main.py

# 3. Select Web Mode [2]
Your choice [1/2]: 2

# 4. Use defaults [2]
Your choice [1/2]: 2

# 5. Open browser to http://127.0.0.1:5000

# 6. Click microphone and speak!
```

That's it! You're ready to use the voice assistant in web mode. Enjoy! 🎉
