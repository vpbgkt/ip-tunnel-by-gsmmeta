# Release Checklist - IP Tunnel by GsmMeta

## Pre-Release Testing

### 1. Functional Testing
- [ ] SSH key generation works
- [ ] Public key copies to clipboard
- [ ] Server command saves correctly
- [ ] Connection establishes successfully
- [ ] Green/red status indicator works
- [ ] Disconnect works properly
- [ ] Auto-connect on startup functions
- [ ] Settings save and load correctly
- [ ] Configuration reset works
- [ ] Window resizing (setup vs connection view) works
- [ ] Scrollable setup view displays all content

### 2. UI/UX Testing
- [ ] All buttons visible and clickable
- [ ] Text is readable
- [ ] Logo displays correctly in title bar
- [ ] No UI elements overlap
- [ ] Proper error messages shown
- [ ] Confirmation dialogs work

### 3. Error Handling
- [ ] SSH client not found - proper error message
- [ ] Invalid server command - validation works
- [ ] Network disconnection - handled gracefully
- [ ] Rapid connect/disconnect - no crashes
- [ ] File permissions issues - handled

### 4. Platform Testing
- [ ] Windows 10 (tested)
- [ ] Windows 11 (tested)
- [ ] Windows 8.1 (if possible)
- [ ] Windows 7 (if possible)

### 5. Build Testing
- [ ] `python test_system.py` passes all tests
- [ ] `python main.py` runs without errors
- [ ] `python build_exe.py` creates executable
- [ ] Executable runs on clean Windows system
- [ ] Icon displays in taskbar
- [ ] Icon displays in executable file
- [ ] No console window appears

## Documentation Review

- [ ] README.md is complete and accurate
- [ ] USER_GUIDE.md is up to date
- [ ] DEVELOPER.md has correct information
- [ ] CONTRIBUTING.md is present
- [ ] LICENSE file is included
- [ ] All code has proper docstrings
- [ ] Version number is updated

## Build Process

### Creating Release Executable

```bash
# 1. Ensure logo.png is present
# 2. Run build script
python build_exe.py

# 3. Test the executable
cd dist
.\IP_Tunnel_GsmMeta.exe

# 4. Verify icon
# - Check taskbar icon
# - Check file icon in Explorer
```

### Files to Include in Release

```
IP_Tunnel_GsmMeta_v1.0.0/
├── IP_Tunnel_GsmMeta.exe    # Main executable
├── README.md                 # Quick start guide
├── USER_GUIDE.md            # Detailed manual
└── LICENSE                  # MIT License
```

## GitHub Release Steps

1. **Create Release Tag**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. **Create GitHub Release**
   - Go to repository → Releases → New Release
   - Tag: v1.0.0
   - Title: IP Tunnel by GsmMeta v1.0.0
   - Description: See CHANGELOG.md
   - Attach: `IP_Tunnel_GsmMeta.exe`
   - Attach: Documentation files

3. **Update README Badges**
   - Latest release version
   - Download count

## Post-Release

- [ ] Announcement on relevant channels
- [ ] Monitor issues for bug reports
- [ ] Respond to user questions
- [ ] Plan next release features

## Version Numbering

Format: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

Current: **1.0.0**

## Distribution Checklist

### For GitHub
- [ ] Source code repository public
- [ ] All dependencies listed in requirements.txt
- [ ] Clear installation instructions
- [ ] Issue tracker enabled
- [ ] Contributing guidelines present

### For End Users
- [ ] Single executable file
- [ ] No installation required
- [ ] Clear usage instructions
- [ ] Support contact information
- [ ] FAQ for common issues

## Security Considerations

- [ ] No hardcoded credentials
- [ ] Private keys never transmitted
- [ ] Secure configuration storage
- [ ] Input validation on server commands
- [ ] Safe error messages (no sensitive data)

---

**Release Manager**: _______________  
**Date**: _______________  
**Approved**: [ ]
