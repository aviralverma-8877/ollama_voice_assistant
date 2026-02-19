# HTTPS/SSL Setup Guide

This guide shows you how to enable HTTPS for the voice assistant web server using a self-signed SSL certificate.

## 🔐 Why Use HTTPS?

- **Security**: Encrypted communication between browser and server
- **Required Features**: Some browser features (like microphone access on remote devices) may require HTTPS
- **Best Practice**: HTTPS is the modern standard for web applications

## ⚠️ Important Note

This guide uses **self-signed certificates** which are suitable for:
- Local development
- Testing
- Private networks
- Internal use

**NOT suitable for:**
- Public websites
- Production environments
- Internet-facing servers

Browsers will show a security warning for self-signed certificates - this is expected and normal.

## 🚀 Quick Start

### Step 1: Generate SSL Certificate

Run the certificate generation script:

```bash
python generate_cert.py
```

The script will:
1. Check if certificates already exist
2. Ask for hostname (default: localhost)
3. Ask for validity period (default: 365 days)
4. Generate `cert.pem` (certificate) and `key.pem` (private key)

**Example output:**
```
🔐 SSL Certificate Generator

Detected local IP: 192.168.1.109

Enter hostname for certificate (press Enter for localhost):
  Suggestions: localhost, 192.168.1.109, or your domain name

Hostname: localhost

Enter number of days the certificate should be valid (default: 365):
Days: 365

[1/4] Generating private key...
✓ Private key generated

[2/4] Generating certificate...
✓ Certificate generated

[3/4] Saving private key to key.pem...
✓ Private key saved

[4/4] Saving certificate to cert.pem...
✓ Certificate saved

✓ SSL Certificate Generation Complete!
```

### Step 2: Start Server with HTTPS

```bash
python main.py
```

Select Web Mode [2], and you'll see:

```
🔐 Protocol Selection

✓ SSL certificates found
   Certificate: cert.pem
   Private Key: key.pem

Choose protocol:
  [1] HTTP  - Standard (no SSL, no browser warnings)
  [2] HTTPS - Secure (encrypted, requires SSL certificates)

Your choice [1/2]: 2
```

Select [2] to enable HTTPS.

**If certificates don't exist:**

If you try to select HTTPS without certificates, you'll see:

```
🔐 Protocol Selection

⚠️  SSL certificates not found
   To use HTTPS, generate certificates first:
   Run: python generate_cert.py

Choose protocol:
  [1] HTTP  - Standard (no SSL, no browser warnings)
  [2] HTTPS - Secure (encrypted, requires SSL certificates)

Your choice [1/2]: 2

❌ Cannot use HTTPS - certificates not found

Options:
  [1] Continue with HTTP
  [2] Exit and generate certificates first
```

Select [2] to exit and run `python generate_cert.py` first, or [1] to continue with HTTP.

### Step 3: Access the Server

The server will display:

```
🌐 VOICE ASSISTANT WEB SERVER (HTTPS)

🔗 Access the web interface from:
   • Local:   https://localhost:5000
   • Network: https://192.168.1.109:5000

💡 Share the network URL with other devices on your local network

🔐 SSL/TLS enabled
   Certificate: cert.pem
   ⚠️  Self-signed certificate - browsers will show security warning
```

### Step 4: Accept Browser Security Warning

When you first visit the HTTPS URL:

**Chrome/Edge:**
1. You'll see "Your connection is not private"
2. Click "Advanced"
3. Click "Proceed to localhost (unsafe)"

**Firefox:**
1. You'll see "Warning: Potential Security Risk Ahead"
2. Click "Advanced"
3. Click "Accept the Risk and Continue"

**Safari:**
1. You'll see "This Connection Is Not Private"
2. Click "Show Details"
3. Click "visit this website"
4. Enter your password if prompted

This warning is expected for self-signed certificates and is safe to bypass on your local network.

## 📋 Detailed Configuration

### Generate Certificate with Custom Settings

```bash
python generate_cert.py
```

**Hostname Options:**
- `localhost` - For local access only
- `192.168.1.109` - Your network IP (for network access)
- `*.local` - Wildcard for local network
- `myserver.local` - Custom hostname

**Validity Period:**
- Default: 365 days (1 year)
- Longer: 730 days (2 years), 3650 days (10 years)
- The certificate expires after this period

### Enable HTTPS by Default

Edit `src/config.py`:

```python
# Web Server SSL/HTTPS Configuration
USE_HTTPS = True  # Set to True to enable HTTPS by default
SSL_CERT_FILE = "cert.pem"  # Path to SSL certificate file
SSL_KEY_FILE = "key.pem"  # Path to SSL private key file
```

With `USE_HTTPS = True`, the server will automatically prompt for HTTPS if certificates exist.

### Custom Certificate Paths

If you want to use certificates from a different location:

```python
SSL_CERT_FILE = "/path/to/your/cert.pem"
SSL_KEY_FILE = "/path/to/your/key.pem"
```

### Regenerate Certificates

To create new certificates (e.g., after expiry):

```bash
# Delete old certificates
rm cert.pem key.pem

# Generate new ones
python generate_cert.py
```

## 🛠️ Troubleshooting

### Certificate Generation Fails

**Error: cryptography module not found**

The script will automatically install it:
```bash
pip install cryptography
```

Then run the script again.

**Error: Permission denied**

Make sure you have write permissions in the current directory.

### Browser Still Shows Warning

This is **normal** for self-signed certificates. The warning means:
- The certificate is not signed by a trusted Certificate Authority
- The connection is still encrypted
- Safe for local/private networks

### HTTPS Not Working

**Check 1: Certificates exist**
```bash
ls -la cert.pem key.pem
```

Both files should be present in the project root.

**Check 2: Certificates are valid**
```bash
openssl x509 -in cert.pem -text -noout
```

Should show certificate details.

**Check 3: Port is not blocked**

HTTPS uses the same port as HTTP (5000 by default). Make sure:
- Firewall allows the port (run `allow_firewall.bat`)
- No other service is using the port

### "SSL Certificate Verify Failed" Error

This error occurs when Python can't verify the certificate. This is normal for self-signed certificates.

**For external API calls from the server:**
You may need to disable SSL verification (development only):
```python
requests.get(url, verify=False)
```

### Mixed Content Errors

If your HTTPS site loads HTTP resources, browsers block them. Ensure all resources (CSS, JS, images) use HTTPS or relative URLs.

## 🔒 Security Best Practices

### For Development/Local Use

✅ **Good:**
- Using self-signed certificates on local network
- HTTPS for localhost testing
- Private network deployment

❌ **Bad:**
- Deploying self-signed certs to public internet
- Sharing private keys
- Using same certificate across multiple servers

### For Production/Public Use

If you need a public HTTPS server:

1. **Get a proper SSL certificate:**
   - Let's Encrypt (free, automated)
   - Commercial Certificate Authority
   - Cloud provider certificates

2. **Use a proper domain:**
   - Register a domain name
   - Configure DNS properly
   - Get certificate for that domain

3. **Use a reverse proxy:**
   - nginx or Apache with SSL
   - Cloud load balancer with SSL
   - Cloudflare (handles SSL for you)

### Certificate Management

**DO:**
- Keep private keys secure
- Set appropriate expiry dates
- Regenerate certificates regularly
- Use strong key sizes (2048-bit minimum)

**DON'T:**
- Commit private keys to version control (already in .gitignore)
- Share private keys via email/chat
- Reuse the same certificate everywhere
- Use expired certificates

## 📱 Mobile Access with HTTPS

### Install Certificate on Mobile (Optional)

For a better mobile experience without warnings:

**iOS:**
1. Email cert.pem to yourself
2. Open on iOS device
3. Go to Settings → Profile Downloaded
4. Install the profile
5. Go to Settings → General → About → Certificate Trust Settings
6. Enable full trust for the certificate

**Android:**
1. Copy cert.pem to device
2. Go to Settings → Security → Install from storage
3. Select the certificate
4. Name it and install

This is **optional** - the connection is still encrypted without this step.

## 🔄 HTTP vs HTTPS Comparison

| Feature | HTTP | HTTPS |
|---------|------|-------|
| **Encryption** | No | Yes (TLS/SSL) |
| **Browser Warning** | No | Yes (self-signed) |
| **Port** | 5000 | 5000 |
| **Setup** | None | Generate certificate |
| **Speed** | Slightly faster | Slightly slower (negligible) |
| **Best For** | Local testing | Local network, development |

## 💡 Tips

1. **Certificate Expiry**: Set a reminder to regenerate certificates before they expire

2. **Network Access**: Use your network IP in the certificate for network access:
   ```bash
   Hostname: 192.168.1.109
   ```

3. **Multiple Hostnames**: Generate separate certificates for different access methods

4. **Testing**: Test both HTTP and HTTPS to see which works better for your use case

5. **Browser Bookmarks**: After accepting the certificate warning once, bookmark the page for easy access

## 📚 Additional Resources

- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [SSL Labs Testing](https://www.ssllabs.com/ssltest/)
- [Let's Encrypt](https://letsencrypt.org/) (for production certificates)
- [Python cryptography documentation](https://cryptography.io/)

## 🆘 Need Help?

If you encounter issues:

1. Check this guide's troubleshooting section
2. Verify certificates exist and are valid
3. Try HTTP mode first to isolate SSL issues
4. Check browser console for specific errors
5. See [NETWORK_ACCESS.md](NETWORK_ACCESS.md) for firewall/network issues

---

**Remember**: Self-signed certificates are perfect for local development and private networks, but not for public websites!
