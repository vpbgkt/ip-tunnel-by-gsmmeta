# Changelog

All notable changes to GsmMeta Server will be documented in this file.

## [2.0.0] - 2026-01-17

### 🎨 Complete Redesign
- Migrated from Python to .NET 8 WPF for better performance
- New modern UI with pill-style navigation
- Hero-centered connection status display (110px indicator)
- Dark theme with professional color palette
- Fixed window size (360x540) with no scrolling needed
- 8px rounded corners on all controls

### ⚡ Performance Improvements
- **83% smaller app size**: 8.3 MB (framework-dependent) vs 48 MB (Python/PyInstaller)
- **50% less memory**: ~40 MB vs ~80 MB Python version
- Faster startup time with native compiled code
- Real-time connection monitoring with 2-second intervals

### ✨ New Features
- One-click SSH key generation (RSA 2048-bit)
- Clipboard integration for public key copying
- Persistent configuration saved in AppData
- Auto-connect on startup option
- Comprehensive system logs with copy/clear functionality
- Visual connection status with automatic disconnect detection

### 🛠️ Technical Changes
- Built with .NET 8 and WPF
- PowerShell integration for SSH tunnel management
- JSON-based configuration storage
- Async/await patterns for responsive UI
- Custom WPF styles and control templates

### 📦 Build Options
- **Framework-dependent**: 8.3 MB (requires .NET 8 Runtime)
- **Self-contained**: 165 MB (no runtime needed)

### 🗑️ Removed
- Python codebase and dependencies
- PyInstaller build system
- MaterialDesign XAML dependencies
- Old documentation (DEVELOPER.md, USER_GUIDE.md, etc.)

---

## [1.0.0] - 2025-12-XX

### Initial Python Release
- Basic SSH tunnel functionality
- PyInstaller-based Windows executable
- Simple tkinter-based UI
- Manual configuration management
