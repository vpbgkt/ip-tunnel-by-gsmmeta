# GsmMeta Server

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![.NET Version](https://img.shields.io/badge/.NET-8.0-blue)](https://dotnet.microsoft.com/download/dotnet/8.0)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)](https://www.microsoft.com/windows)

**Modern SSH tunnel manager for USB port sharing - Built with .NET 8 & WPF**

![GsmMeta Server](logo.png)

## 🎨 Modern UI Features

- **Pill-Style Navigation** - Clean toggle between Connection and Settings
- **Hero Status Display** - Large 110px circular connection indicator  
- **Always-Visible Controls** - 50px connect button, no scrolling required
- **Optimal Window Size** - 360x540, perfectly sized for desktop use
- **Professional Design** - 8px rounded corners, #3478F6 accent color
- **Dark Theme** - Easy on the eyes with high-contrast white text

## 🌟 Features

- **🔑 One-Click SSH Key Generation** - Generate RSA 2048-bit key pairs instantly
- **📋 Clipboard Integration** - Copy public keys with a single click
- **💾 Persistent Configuration** - Saves server commands securely in AppData
- **🔄 Real-Time Status Monitoring** - Visual connection status with automatic disconnect detection
- **⚡ Auto-Connect** - Optional automatic connection on startup
- **📝 System Logs** - Comprehensive logging with copy/clear functionality
- **🪟 Windows Native** - PowerShell integration, lightweight and fast

## 🚀 Quick Start

### For End Users

**1. Install .NET 8 Runtime** (one-time requirement)
   - Download: [.NET 8 Desktop Runtime](https://dotnet.microsoft.com/download/dotnet/8.0)
   - Size: ~55 MB
   - Takes 2 minutes

**2. Download & Run**
   - Get the latest release from [Releases](https://github.com/vpbgkt/ip-tunnel-by-gsmmeta/releases)
   - Extract and run `IP_Tunnel_GsmMeta.exe`

### For Developers

#### Prerequisites
- .NET 8 SDK
- Windows 7/8/10/11 (64-bit)
- OpenSSH Client (built-in on Windows 10/11)

#### Build & Run

```powershell
# Clone the repository
git clone https://github.com/vpbgkt/ip-tunnel-by-gsmmeta.git
cd ip-tunnel-by-gsmmeta

# Restore dependencies
dotnet restore

# Run the application
dotnet run

# Or build for release
dotnet build -c Release

# Publish framework-dependent (8.3 MB)
dotnet publish -c Release --output dist

# Publish self-contained (165 MB, no runtime needed)
dotnet publish -c Release -r win-x64 --self-contained true /p:PublishSingleFile=true --output dist
```

## 🎯 How to Use

### Initial Setup

1. Click **Settings** tab
2. Click **Generate Key** under Authentication
3. Click **Copy Key** and send it to GsmMeta support
4. Receive your SSH connection command from support
5. Paste the command in **Connection Command** field
6. Click **Save Configuration**

### Daily Use

1. Switch to **Connection** tab
2. Click the big **CONNECT** button
3. Monitor your connection status
4. *(Optional)* Enable "Auto-connect on startup"

## 📊 Performance

| Metric | Value |
|--------|-------|
| **App Size** | 8.3 MB (framework-dependent) |
| **Startup Time** | <1 second |
| **Memory Usage** | ~40 MB |
| **Runtime Required** | .NET 8 (~55 MB one-time install) |

Compare to Python version: 83% smaller app size, 50% less memory!

## 🛠️ Project Structure

```
ip-tunnel-by-gsmmeta/
├── Managers/
│   ├── SshKeyManager.cs       # SSH key operations
│   ├── ConfigManager.cs       # JSON configuration
│   └── ConnectionManager.cs   # SSH tunnel lifecycle
├── MainWindow.xaml            # Main UI
├── MainWindow.xaml.cs         # UI logic
├── LogsWindow.xaml            # Logs viewer
├── App.xaml                   # App resources & styles
├── IPTunnelGsmMeta.csproj     # Project configuration
└── logo.png                   # Application icon
```

## 📋 System Requirements

- **OS**: Windows 7 SP1 / 8 / 10 / 11 (64-bit)
- **Runtime**: .NET 8 Desktop Runtime
- **SSH**: OpenSSH Client (built-in on Windows 10+)
- **Disk**: ~65 MB (runtime + app)
- **RAM**: 40 MB minimum

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 📞 Support

- **Website**: [gsmmeta.com](https://gsmmeta.com)
- **Issues**: [GitHub Issues](https://github.com/vpbgkt/ip-tunnel-by-gsmmeta/issues)
- **Email**: support@gsmmeta.com

## 🎉 Changelog

### v2.0.0 (January 2026)
- 🎨 Complete UI redesign with modern pill navigation
- 🔄 Migrated from Python to .NET 8 WPF
- ⚡ 83% smaller app size (8.3 MB vs 48 MB)
- 🚀 50% faster startup and lower memory usage
- ✨ Hero-style connection status display
- 🪟 Resizable window with optimal defaults

---

**Made with ❤️ by [GsmMeta.com](https://gsmmeta.com)**  
*Version 2.0.0 - January 2026*
