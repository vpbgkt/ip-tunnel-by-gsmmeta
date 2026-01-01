# 🚀 Quick Setup Guide - IP Tunnel by GsmMeta

## For End Users (Non-Technical)

### Step 1: Download
Download `IP_Tunnel_GsmMeta.exe` from the [latest release](https://github.com/yourusername/ip-tunnel-gsmmeta/releases)

### Step 2: Run
Double-click the executable. If Windows shows a security warning:
1. Click "More info"
2. Click "Run anyway"

### Step 3: Generate SSH Key
1. Click **"Generate SSH Key"** button
2. Wait for confirmation message
3. Click **"Copy Public Key"** button

### Step 4: Get Server Command
1. Email your public key to GsmMeta support
2. Wait for response with server command
3. Copy the command (looks like: `ssh -4 -N -R 0.0.0.0:32032:127.0.0.1:32032 tech2@167.71.148.25`)

### Step 5: Configure
1. Paste the server command into the text box
2. Click **"Save Configuration & Continue"**
3. Window will shrink to compact size

### Step 6: Connect
1. Click **"Connect to Server"** (green button)
2. Wait for status to turn green
3. Your USB tunnel is now active!

### Step 7: Daily Use
- **To connect**: Click the green button
- **To disconnect**: Click the red button
- **Settings**: Click ⚙ Settings for options

---

## For Developers

### Quick Setup

```bash
# Clone repository
git clone https://github.com/yourusername/ip-tunnel-gsmmeta.git
cd ip-tunnel-gsmmeta

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Building Executable

```bash
# Install build tools
pip install pyinstaller

# Build (auto-converts logo.png to .ico)
python build_exe.py

# Find executable
cd dist
# IP_Tunnel_GsmMeta.exe is ready!
```

### Project Files

| File | Purpose |
|------|---------|
| `main.py` | Main GUI application |
| `ssh_key_manager.py` | SSH operations |
| `config_manager.py` | Configuration storage |
| `connection_manager.py` | Tunnel management |
| `build_exe.py` | Executable builder |
| `test_system.py` | System tests |
| `requirements.txt` | Python dependencies |
| `logo.png` | Application logo/icon |

### Testing

```bash
# Run tests
python test_system.py

# Expected: All tests passed!
```

### Development Workflow

1. Make changes to code
2. Test with `python main.py`
3. Run system tests
4. Build executable to verify
5. Test on clean Windows system
6. Submit PR

---

## Troubleshooting

### "SSH client not found"
**Solution**: Enable OpenSSH Client
- Windows 10/11: Settings → Apps → Optional Features → Add OpenSSH Client
- Windows 7/8: Download and install OpenSSH for Windows

### "Connection fails"
**Check**:
- Internet connection working
- Server command is correct
- SSH key was sent to GsmMeta
- Firewall isn't blocking SSH (port 22)

### "Can't save configuration"
**Solution**: Run as Administrator if AppData access is restricted

### Build Issues
```bash
# Update pip
python -m pip install --upgrade pip

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Clear build cache
python build_exe.py  # Includes automatic cleanup
```

---

## System Requirements

**Operating System**:
- Windows 7 SP1 or later
- Windows 10/11 (recommended)

**Dependencies** (for source):
- Python 3.8 or higher
- OpenSSH Client

**Disk Space**:
- Executable: ~15 MB
- Source: ~5 MB

**RAM**: 50 MB minimum

**Network**: Internet connection required

---

## Support

- **📧 Email**: support@gsmmeta.com
- **📖 Documentation**: See USER_GUIDE.md
- **🐛 Issues**: GitHub Issues page
- **💬 Discussions**: GitHub Discussions

---

## What's Next?

1. ✅ Generate SSH key
2. ✅ Submit to GsmMeta
3. ✅ Receive server command
4. ✅ Save configuration
5. ✅ Connect and enjoy!

**Happy USB Sharing!** 🎉
