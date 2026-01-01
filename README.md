# IP Tunnel by GsmMeta

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)](https://www.microsoft.com/windows)

**Professional SSH tunnel manager for USB port sharing over network - eliminating the need for Radmin VPN.**

![IP Tunnel by GsmMeta](logo.png)

## 🌟 Features

- **🔑 One-Click SSH Key Generation** - Generate RSA 2048-bit key pairs instantly
- **📋 Clipboard Integration** - Copy public keys with a single click
- **💾 Persistent Configuration** - Saves server commands securely in AppData
- **🔄 Real-Time Status Monitoring** - Visual connection status with automatic disconnect detection
- **⚡ Auto-Connect** - Optional automatic connection on startup
- **🎨 Modern UI** - Clean, dark-themed interface with CustomTkinter
- **📦 Standalone Executable** - No Python installation required for end users
- **🪟 Windows Native** - PowerShell integration, system tray ready

## 🚀 Quick Start

### For End Users (No Programming Required)

1. **Download** the latest release: `IP_Tunnel_GsmMeta.exe`
2. **Run** the executable (Windows may show a security warning - click "More info" → "Run anyway")
3. **Generate** your SSH key
4. **Submit** your public key to GsmMeta support
5. **Receive** your server connection command
6. **Paste** the command and click "Save Configuration & Continue"
7. **Connect** with one click!

### For Developers

#### Prerequisites
- Python 3.8 or higher
- Windows 7/8/10/11
- OpenSSH Client (built-in on Windows 10/11)

#### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ip-tunnel-gsmmeta.git
cd ip-tunnel-gsmmeta

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 📦 Building from Source

Create a standalone executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable (includes logo as icon)
python build_exe.py

# Find executable in dist/ folder
# Output: dist/IP_Tunnel_GsmMeta.exe
```

The build process automatically:
- Converts `logo.png` to `.ico` format
- Embeds the icon in the executable
- Bundles all dependencies
- Creates a single portable file

## 🎯 Usage Guide

### First-Time Setup

1. **Launch** the application
2. Click **"Generate SSH Key"** to create your key pair
3. Click **"Copy Public Key"** to copy your public key
4. **Contact GsmMeta support** with your public key
5. **Receive** a server command like:
   ```bash
   ssh -4 -N -R 0.0.0.0:32032:127.0.0.1:32032 tech2@167.71.148.25
   ```
6. **Paste** the command into the text box
7. Click **"Save Configuration & Continue"**

### Daily Use

1. **Open** the application
2. Click **"Connect to Server"** (green button)
3. **Status indicator** turns green when connected
4. Click **"Disconnect from Server"** (red button) when finished

### Settings

Access via ⚙ Settings button:
- **Auto-connect on startup** - Enable for always-on sharing
- **Server command** - View or update your connection command
- **Reset configuration** - Return to initial setup

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│         main.py (GUI Application)           │
│   CustomTkinter · Dark Theme · Scrollable  │
└──────────┬──────────────┬──────────────┬────┘
           │              │              │
    ┌──────▼─────┐ ┌─────▼──────┐ ┌────▼──────┐
    │ SSH Key    │ │   Config   │ │Connection │
    │ Manager    │ │  Manager   │ │ Manager   │
    ├────────────┤ ├────────────┤ ├───────────┤
    │ssh-keygen  │ │   AppData  │ │PowerShell │
    │Detection   │ │   JSON     │ │Subprocess │
    │Copy/Paste  │ │  Persist   │ │Monitoring │
    └────────────┘ └────────────┘ └───────────┘
```

### Core Components

| Module | Purpose | Key Features |
|--------|---------|--------------|
| `main.py` | GUI Application | CustomTkinter, scrollable frames, dynamic resizing |
| `ssh_key_manager.py` | SSH Operations | Key generation, detection, retrieval |
| `config_manager.py` | Configuration | AppData persistence, JSON storage |
| `connection_manager.py` | Tunnel Management | PowerShell execution, health monitoring |

## 📁 Project Structure

```
ip-tunnel-gsmmeta/
├── main.py                 # Main GUI application
├── ssh_key_manager.py      # SSH key operations
├── config_manager.py       # Configuration persistence
├── connection_manager.py   # Connection management
├── build_exe.py           # Build script for executable
├── requirements.txt       # Python dependencies
├── logo.png              # Application logo
├── README.md             # This file
├── LICENSE               # MIT License
├── USER_GUIDE.md         # Detailed user manual
└── DEVELOPER.md          # Technical documentation
```

## 🔧 Requirements

### Runtime Requirements
- **Windows** 7, 8, 10, or 11
- **OpenSSH Client** (built-in on Windows 10/11)

### Development Requirements
- **Python** 3.8+
- **customtkinter** ≥5.2.0
- **Pillow** ≥10.0.0
- **pyperclip** ≥1.8.0
- **psutil** ≥5.9.0

## 🧪 Testing

Run system tests:

```bash
# Test all components
python test_system.py

# Expected output:
# ✓ All module imports successful (13/13)
# ✓ SSH client detected
# ✓ Configuration directory created
# ✓ All tests passed!
```

## 🐛 Troubleshooting

### Common Issues

**"SSH client not found"**
- Windows 10/11: Enable OpenSSH via Settings → Apps → Optional Features
- Windows 7/8: Install OpenSSH for Windows manually

**"Connection fails immediately"**
- Verify server command is correct
- Check SSH key is registered with GsmMeta
- Ensure internet connectivity
- Check firewall settings

**"Settings won't save"**
- Run as Administrator if AppData access is restricted
- Check disk space

For more help, see [USER_GUIDE.md](USER_GUIDE.md)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [DEVELOPER.md](DEVELOPER.md) for technical details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CustomTkinter** - Modern GUI framework
- **OpenSSH** - Secure shell implementation
- **GsmMeta** - Server infrastructure

## 📞 Support

- **Email**: support@gsmmeta.com
- **Issues**: [GitHub Issues](https://github.com/yourusername/ip-tunnel-gsmmeta/issues)
- **Documentation**: [USER_GUIDE.md](USER_GUIDE.md)

## 🔄 Version History

### Version 1.0.0 (January 2026)
- ✅ Initial release
- ✅ SSH key generation and management
- ✅ Persistent configuration storage
- ✅ Real-time connection monitoring
- ✅ Modern scrollable UI
- ✅ Standalone executable with logo
- ✅ Auto-connect on startup
- ✅ Settings panel

---

**Made with ❤️ by GsmMeta Team**
