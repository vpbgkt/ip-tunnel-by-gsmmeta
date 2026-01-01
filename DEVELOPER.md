# IP Tunnel by GsmMeta - Developer Documentation

## Project Structure

```
ip tunnel by gsmmeta/
│
├── main.py                    # Main GUI application
├── ssh_key_manager.py         # SSH key generation and management
├── config_manager.py          # Configuration persistence (AppData)
├── connection_manager.py      # SSH tunnel connection handling
│
├── requirements.txt           # Python dependencies
├── build_exe.py              # PyInstaller build script
├── start.py                  # Dependency checker
├── run.bat                   # Windows batch launcher
│
├── README.md                 # Project overview
├── USER_GUIDE.md             # End-user documentation
├── DEVELOPER.md              # This file
└── .gitignore               # Git ignore rules
```

## Architecture

### Module Overview

#### 1. **main.py** - GUI Application
- Built with CustomTkinter for modern UI
- Two-state interface:
  - **Setup View:** SSH key generation + server command input
  - **Connection View:** Connect/disconnect with status monitoring
- Handles all user interactions
- Orchestrates other modules

#### 2. **ssh_key_manager.py** - SSH Key Operations
- Generates SSH key pairs using `ssh-keygen`
- Detects existing keys in `~/.ssh/`
- Reads and provides public key for clipboard
- Manages key deletion

**Key Methods:**
- `generate_ssh_key()` - Creates RSA 2048-bit key pair
- `get_public_key()` - Returns public key content
- `check_ssh_keys_exist()` - Verifies key existence

#### 3. **config_manager.py** - Persistent Configuration
- Stores settings in `%APPDATA%\IPTunnelGsmMeta\config.json`
- Manages server connection command
- Handles auto-connect and other preferences
- Import/export functionality

**Configuration Schema:**
```json
{
  "server_command": "ssh -4 -N -R ...",
  "auto_connect": false,
  "minimize_to_tray": true,
  "show_notifications": true,
  "first_run": true
}
```

#### 4. **connection_manager.py** - SSH Tunnel Management
- Executes SSH commands via PowerShell subprocess
- Background thread monitors process health
- Status callback system for UI updates
- Graceful connection/disconnection

**Connection Flow:**
1. Parse SSH command
2. Execute via PowerShell with `CREATE_NO_WINDOW` flag
3. Start monitoring thread
4. Detect disconnections and notify UI
5. Cleanup on disconnect

## Technologies Used

### Core Dependencies
- **CustomTkinter 5.2.1** - Modern UI framework (dark mode, rounded widgets)
- **Pillow 10.1.0** - Image handling for CustomTkinter
- **pyperclip 1.8.2** - Clipboard operations
- **psutil 5.9.6** - Process management

### Build Tools
- **PyInstaller** - Creates standalone executable
- **subprocess** - PowerShell command execution
- **threading** - Background connection monitoring

## Building and Distribution

### Development Mode
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Creating Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
python build_exe.py

# Output: dist/IP_Tunnel_GsmMeta.exe
```

### PyInstaller Configuration
- **Mode:** `--onefile` (single executable)
- **Window:** `--windowed` (no console)
- **Hidden imports:** CustomTkinter, PIL
- **Icon:** Optional `icon.ico` if present

## Key Features Implementation

### 1. SSH Key Generation
```python
# Uses system ssh-keygen command
ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa -N ""
```

### 2. SSH Tunnel Connection
```python
# Executed via PowerShell
powershell.exe -NoProfile -NonInteractive -Command "ssh -4 -N -R ..."
```

### 3. Status Monitoring
- Background thread checks process every 2 seconds
- Uses `process.poll()` to detect termination
- Callback updates UI in main thread via `after()`

### 4. Configuration Persistence
- JSON file in AppData (survives app updates)
- Automatic directory creation
- Graceful error handling

## User Workflow

### First-Time User Flow
1. Launch app → Setup View
2. Generate SSH key → Copy public key
3. Provide key to GsmMeta → Receive server command
4. Paste server command → Save
5. Switch to Connection View

### Returning User Flow
1. Launch app → Connection View (command already saved)
2. Click Connect → SSH tunnel starts
3. Green status indicator
4. Click Disconnect when done

### Settings Flow
1. Click Settings button
2. Modify auto-connect or server command
3. Save → Refresh view
4. Optional: Reset configuration (returns to setup)

## Error Handling

### SSH Client Not Found
- Windows 10/11: Should never happen (built-in OpenSSH)
- Windows 7/8: User must install OpenSSH
- Error shown with instructions

### Connection Failures
- Invalid command format
- Authentication failure (key not registered)
- Network unreachable
- Server down

All errors captured from stderr and shown to user.

### Process Monitoring
- Detects unexpected disconnections
- Updates UI automatically
- Captures termination errors

## Security Considerations

### SSH Key Management
- Keys generated in standard `~/.ssh/` location
- No passphrase (for automation)
- Private key never transmitted
- Only public key shared with server

### Connection Security
- All traffic encrypted via SSH
- Direct SSH tunnel (no intermediaries)
- Command validation (must start with "ssh")
- No credential storage except SSH keys

### Configuration Security
- Config stored in user's AppData
- No passwords or sensitive data in config
- Server command visible to user

## Customization Points

### UI Themes
```python
# In main.py
ctk.set_appearance_mode("dark")  # or "light", "system"
ctk.set_default_color_theme("blue")  # or "green", "dark-blue"
```

### Default Ports
Currently hardcoded in user's server command.
Could add port configuration UI if needed.

### Auto-Reconnect
Not implemented. Could add:
```python
def auto_reconnect(self):
    max_retries = 5
    retry_delay = 5  # seconds
    # Implementation...
```

### System Tray
Not implemented. Could add using `pystray`:
```python
# Minimize to tray instead of closing
# Right-click menu: Connect, Disconnect, Exit
```

## Testing

### Manual Testing Checklist
- [ ] SSH key generation works
- [ ] Public key copies to clipboard
- [ ] Server command saves correctly
- [ ] Connection establishes successfully
- [ ] Green indicator shows when connected
- [ ] Disconnect works properly
- [ ] Auto-connect on startup
- [ ] Settings save and load
- [ ] Reset configuration works
- [ ] Window close while connected prompts

### Edge Cases
- No SSH client installed
- Invalid server command
- Network disconnection during tunnel
- Rapid connect/disconnect
- Multiple instances (config sharing)

## Known Limitations

1. **Windows Only** - PowerShell-specific implementation
2. **Single Tunnel** - No multi-connection support
3. **No Logging** - Errors only shown in dialogs
4. **No Auto-Reconnect** - Manual reconnection required
5. **No System Tray** - Closes completely on X

## Future Enhancements

### High Priority
- [ ] Logging to file for debugging
- [ ] Auto-reconnect with exponential backoff
- [ ] System tray integration
- [ ] Connection history/logs viewer

### Medium Priority
- [ ] Multiple tunnel profiles
- [ ] Bandwidth monitoring
- [ ] Connection time tracking
- [ ] Toast notifications

### Low Priority
- [ ] Linux/Mac support
- [ ] Custom SSH key locations
- [ ] SSH key with passphrase
- [ ] Import/export configurations

## Troubleshooting Development Issues

### CustomTkinter Import Errors
```bash
pip install --upgrade customtkinter pillow
```

### PyInstaller Missing Modules
Add to `build_exe.py`:
```python
--hidden-import modulename
```

### PowerShell Execution Fails
Check Windows ExecutionPolicy:
```powershell
Get-ExecutionPolicy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Process Not Terminating
Ensure proper cleanup in `connection_manager.py`:
```python
process.terminate()
process.wait(timeout=3)
process.kill()  # Force if needed
```

## Contributing

### Code Style
- PEP 8 compliant
- Type hints recommended
- Docstrings for all public methods
- Comments for complex logic

### Commit Guidelines
- Descriptive commit messages
- One feature per commit
- Test before committing

### Pull Requests
- Include description of changes
- Update documentation if needed
- Test on Windows 10/11

## License
[Specify license - MIT, GPL, Proprietary, etc.]

## Support
For technical support or questions:
- Developer: [Your name/contact]
- GsmMeta: [Support contact]

---

**Version:** 1.0  
**Last Updated:** January 2026
