# Network Access Guide

This guide helps you set up network access for the Ollama Voice Assistant web server, so you can connect from other devices (phones, tablets, laptops) on your local network.

## 🚀 Quick Setup

### Step 1: Start the Web Server

The web server is configured to listen on all network interfaces by default (`0.0.0.0`).

```bash
python main.py
# Select [2] Web Mode
# Use default settings [2]
```

### Step 2: Configure Windows Firewall

**Windows Firewall blocks incoming connections by default.** You need to allow port 5000:

#### Option A: Automatic (Recommended)

Right-click `allow_firewall.bat` and select **"Run as administrator"**

This creates a firewall rule allowing incoming connections on port 5000.

#### Option B: Manual Configuration

1. Open **Windows Defender Firewall with Advanced Security**
2. Click **Inbound Rules** → **New Rule**
3. Select **Port** → Click Next
4. Select **TCP** and enter port **5000** → Click Next
5. Select **Allow the connection** → Click Next
6. Check all profiles (Domain, Private, Public) → Click Next
7. Name: "Ollama Voice Assistant Web Server" → Click Finish

### Step 3: Find Your IP Address

The server automatically displays your network IP addresses when it starts:

```
🔗 Access the web interface from:
   • Local:   http://localhost:5000
   • IPv4:    http://192.168.1.100:5000
   • IPv6:    http://[fe80::1234:5678:90ab:cdef]:5000

💡 Share the network URL with other devices on your local network
```

**Note:** Both IPv4 and IPv6 addresses are shown when available.

Or find them manually:

```bash
# Windows
ipconfig

# Look for:
# - "IPv4 Address" (e.g., 192.168.1.100)
# - "IPv6 Address" (e.g., fe80::1234:5678:90ab:cdef)
```

### Step 4: Connect from Other Devices

1. Connect your device (phone/tablet) to the **same WiFi network**
2. Open a web browser
3. Go to: `http://YOUR-IP:5000` (use the network IP from Step 3)
4. Start using the voice assistant!

## 🛠️ Troubleshooting

### Can't Connect from Another Device

**Check 1: Firewall Rule**
```bash
# Check if firewall rule exists
netsh advfirewall firewall show rule name="Ollama Voice Assistant Web Server"

# If not found, run allow_firewall.bat as administrator
```

**Check 2: Same Network**
- Ensure both devices are on the same WiFi network
- Corporate/Guest networks may block device-to-device communication

**Check 3: Server is Running**
- Make sure the web server is running
- Check that it says "Host: 0.0.0.0" in the startup message

**Check 4: Correct IP Address**
- Use the IP shown by the server
- Don't use `localhost` or `127.0.0.1` from other devices

**Check 5: Antivirus/Security Software**
- Some antivirus programs may block incoming connections
- Temporarily disable or add exception for Python/Flask

### Connection Refused Error

**Cause:** Firewall is blocking the connection

**Solution:**
1. Run `allow_firewall.bat` as administrator
2. Or add firewall rule manually (see Step 2)

### Timeout Error

**Cause:** Server not reachable or wrong IP address

**Solutions:**
1. Verify server is running
2. Check IP address is correct
3. Ping the server from the client device:
   ```bash
   ping 192.168.1.100
   ```
4. Make sure both devices are on same network

### Corporate/Public WiFi Issues

**Problem:** Some networks block device-to-device communication

**Solutions:**
1. Use a personal WiFi network/hotspot
2. Connect both devices via USB tethering
3. Use a router you control

## 🔒 Security Considerations

### Local Network Only

The server only accepts connections from your local network. It is **not exposed to the internet**.

### No Authentication

The web interface has no password protection. Anyone on your local network can access it.

**Best Practices:**
- Only use on trusted networks (home/office)
- Don't use on public WiFi
- Close the server when not in use

### Firewall Protection

The firewall rule only allows incoming TCP connections on port 5000. This is a standard web server port.

To remove network access:
1. Stop the web server
2. Run `remove_firewall.bat` as administrator

## 📱 Testing Network Access

### From the Same Computer

```bash
# Test localhost
curl http://localhost:5000/api/status

# Test network interface
curl http://YOUR-IP:5000/api/status
```

### From Another Device (Phone/Tablet)

1. Open web browser
2. Go to: `http://YOUR-IP:5000`
3. You should see the voice assistant interface

### Using Command Line

From another computer on the network:

```bash
# Windows
curl http://192.168.1.100:5000/api/status

# Linux/Mac
curl http://192.168.1.100:5000/api/status
```

Expected response:
```json
{
  "status": "running",
  "wake_word": "computer",
  "model": "gemma3:4b",
  "messages_in_history": 0
}
```

## 🔧 Advanced Configuration

### Change Port

If port 5000 is in use:

1. Start the server
2. Select Web Mode [2]
3. Select custom settings [1]
4. Enter a different port (e.g., 8080)
5. Update firewall rule:
   ```bash
   netsh advfirewall firewall add rule name="Ollama Voice Assistant Custom Port" dir=in action=allow protocol=TCP localport=8080
   ```

### Restrict to Localhost Only

If you only want local access:

1. Start the server
2. Select Web Mode [2]
3. Select custom settings [1]
4. Enter host: `127.0.0.1`
5. No firewall rule needed (only local access)

### Multiple Network Interfaces

If you have multiple network adapters (WiFi + Ethernet), the server binds to all interfaces (0.0.0.0). You can access it via any of your IP addresses.

### IPv6 Support

The server supports both IPv4 and IPv6 simultaneously (dual-stack):

**IPv6 Address Format:**
- IPv6 addresses in URLs must be enclosed in brackets
- Example: `http://[fe80::1]:5000`
- The server automatically displays the correct format

**Finding Your IPv6 Address:**
```bash
# Windows
ipconfig

# Look for "IPv6 Address" or "Link-local IPv6 Address"
# Example: fe80::1234:5678:90ab:cdef%12
```

**Using IPv6:**
1. The server shows your IPv6 address when it starts
2. Copy the entire URL including brackets
3. Access from other devices on the same network

**IPv6 Notes:**
- Link-local addresses (fe80::) work only on the same network segment
- Global IPv6 addresses work across the internet (if firewall allows)
- Most modern devices support IPv6 automatically

## ❓ FAQ

**Q: Do I need to configure firewall every time?**
A: No, only once. The firewall rule persists until you remove it.

**Q: Can I access from the internet?**
A: No, only from your local network. This is by design for security.

**Q: Why can't my phone connect?**
A: Most common reasons:
- Not on the same WiFi network
- Firewall not configured
- Using localhost instead of network IP

**Q: Is it secure?**
A: It's secure for trusted local networks. Don't use on public WiFi.

**Q: Can multiple devices connect simultaneously?**
A: Yes! Multiple devices can access the web interface at the same time.

**Q: Does this work with mobile hotspot?**
A: Yes, if you create a hotspot from your phone and connect your computer to it.

## 📋 Quick Checklist

Before connecting from another device:

- [ ] Web server is running with default settings (0.0.0.0)
- [ ] Firewall rule is added (run allow_firewall.bat)
- [ ] Both devices on same WiFi network
- [ ] Using correct network IP (not localhost)
- [ ] No VPN or proxy interfering

## 🎯 Summary

1. **Start server** with default settings
2. **Add firewall rule** (allow_firewall.bat as admin)
3. **Note the network IP** shown by server
4. **Connect from other device** using that IP
5. **Enjoy** your voice assistant on any device!

For more help, see [WEB_MODE_GUIDE.md](WEB_MODE_GUIDE.md).
