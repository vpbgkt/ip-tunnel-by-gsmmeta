# Changelog

All notable changes to IP Tunnel by GsmMeta will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-01

### Added
- Initial release
- SSH key generation with one-click copy to clipboard
- Persistent server configuration storage in AppData
- Real-time SSH tunnel connection monitoring
- Modern dark-themed UI with CustomTkinter
- Scrollable setup view for all screen sizes
- Dynamic window resizing (600x600 setup, 320x200 connection)
- Single toggle button for connect/disconnect
- Visual status indicator (green/red dot)
- Auto-connect on startup option
- Settings panel with configuration management
- Logo integration in window icon and taskbar
- Standalone executable build with PyInstaller
- PowerShell-based SSH execution
- Background process monitoring
- Graceful error handling
- Configuration reset capability
- MIT License

### Documentation
- Comprehensive README.md for GitHub
- Detailed USER_GUIDE.md with troubleshooting
- Technical DEVELOPER.md documentation
- Contributing guidelines
- Release checklist
- System test suite

### Technical
- Python 3.8+ support
- Windows 7/8/10/11 compatibility
- CustomTkinter 5.2.0+ framework
- Modular architecture (4 core modules)
- Thread-safe connection monitoring
- JSON-based configuration
- No external server dependencies (user provides SSH command)

### Known Limitations
- Windows only (PowerShell-specific)
- Single tunnel connection at a time
- Requires OpenSSH client
- No automatic reconnection (manual only)

## [Unreleased]

### Planned Features
- System tray integration
- Auto-reconnect with exponential backoff
- Connection logs viewer
- Multiple tunnel profiles
- Linux/Mac support
- Toast notifications
- Connection statistics

---

For full details, see [README.md](README.md) and [USER_GUIDE.md](USER_GUIDE.md).
