# User Guide - IP Tunnel by GsmMeta

## Overview
IP Tunnel by GsmMeta is a Windows desktop application that manages SSH tunnels for USB port sharing over the network, eliminating the need for Radmin VPN.

## System Requirements
- **Operating System:** Windows 7, 8, 10, or 11
- **OpenSSH Client:** Built-in on Windows 10/11, may need installation on Windows 7/8
- **Python:** 3.8 or later (only if running from source)

## Installation

### Option 1: Standalone Executable (Recommended)
1. Download `IP_Tunnel_GsmMeta.exe`
2. Double-click to run (no installation needed)
3. Windows may show a security warning - click "More info" → "Run anyway"

### Option 2: Run from Source Code
1. Install Python 3.8+ from [python.org](https://www.python.org)
2. Download/clone the source code
3. Open terminal in the project folder
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the application:
   ```bash
   python main.py
   ```
   Or simply double-click `run.bat`

## First-Time Setup

### Step 1: Generate SSH Key
1. Launch the application
2. Click **"Generate SSH Key"** button
3. The application will create an SSH key pair in `C:\Users\YourName\.ssh\`
4. Click **"Copy Public Key"** to copy your public key to clipboard

### Step 2: Obtain Server Connection Command
1. Contact GsmMeta support with your public key
2. Provide your copied SSH public key
3. GsmMeta will provide you with a server connection command like:
   ```
   ssh -4 -N -R 0.0.0.0:32032:127.0.0.1:32032 tech2@167.71.148.25
   ```

### Step 3: Configure the Application
1. Paste the server command into the text box in the application
2. Click **"Save Configuration & Continue"**
3. The application will switch to the connection view

## Using the Application

### Connecting to the Server
1. Open the application
2. Click **"Connect to Server"** button
3. Watch the status indicator:
   - **Green dot** = Connected
   - **Red dot** = Disconnected
4. Once connected, your USB port is shared via the tunnel

### Disconnecting
1. Click the **"Disconnect"** button
2. The tunnel will close and USB sharing will stop

### Connection Status
- **Green indicator:** Successfully connected to server
- **Red indicator:** Not connected or connection lost
- Status text shows current state and any error messages

## Settings

Click the **⚙ Settings** button to access:

### Auto-Connect on Startup
- Enable to automatically connect when the application starts
- Useful for always-on USB sharing scenarios

### Server Connection Command
- View and modify your server command
- Useful if GsmMeta provides a new command or different port

### Reset Configuration
- Returns to initial setup screen
- Clears saved server command
- Useful for troubleshooting or reconfiguration

## Common Scenarios

### Scenario 1: Daily USB Sharing
1. Open the application
2. Click "Connect to Server" 
3. Use your USB device on the remote computer
4. Click "Disconnect" when finished

### Scenario 2: Always-On Sharing
1. Enable "Auto-connect on startup" in Settings
2. Add the application to Windows startup folder
3. USB will be shared automatically when your computer boots

### Scenario 3: Changing Servers or Ports
1. Contact GsmMeta for new server command
2. Open Settings → Update server command
3. Save and reconnect

## Troubleshooting

### "SSH client not found" Error
- **Windows 10/11:** OpenSSH should be built-in
- **Windows 7/8:** Install OpenSSH:
  1. Download OpenSSH for Windows
  2. Add to system PATH
  3. Restart the application

### Connection Immediately Fails
- Verify the server command is correct
- Check internet connectivity
- Ensure firewall isn't blocking SSH (port 22)
- Contact GsmMeta support to verify your SSH key is registered

### "Process terminated immediately"
Common causes:
- Incorrect SSH key (not registered with server)
- Wrong server address or port
- Network firewall blocking connection
- Server is down or unreachable

**Solution:** Check the error message shown and contact GsmMeta support

### Connection Drops Frequently
- Check internet stability
- Verify server is operational (contact GsmMeta)
- Try reconnecting

### Public Key Won't Copy
- Ensure SSH keys are generated first
- Check clipboard permissions
- Manually navigate to `C:\Users\YourName\.ssh\id_rsa.pub` and copy contents

## File Locations

### Configuration
- **Config file:** `%APPDATA%\IPTunnelGsmMeta\config.json`
- **SSH keys:** `C:\Users\YourName\.ssh\`
  - Private key: `id_rsa`
  - Public key: `id_rsa.pub`

### Logs
- Application errors are shown in message boxes
- PowerShell errors are captured and displayed

## Security Notes

### SSH Key Security
- **Never share your private key** (`id_rsa`)
- Only share the **public key** (`id_rsa.pub`)
- Keep your private key secure and backed up
- If compromised, generate new keys and notify GsmMeta

### Connection Security
- All traffic is encrypted via SSH tunnel
- Only you and GsmMeta server can decrypt the data
- Ensure your server command is from GsmMeta (verify domain/IP)

## Support

### Getting Help
- Email: support@gsmmeta.com (verify actual contact)
- Include in support request:
  - Your public SSH key
  - Error messages (screenshot)
  - Server command you're using
  - Windows version

### Known Limitations
- Only works with USB Redirector or compatible software
- Requires active internet connection
- One tunnel connection at a time
- Windows only (no Mac/Linux support in this version)

## Building Your Own Executable

If you want to create the standalone executable yourself:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run the build script:
   ```bash
   python build_exe.py
   ```

3. Find the executable in the `dist` folder

## FAQ

**Q: Do I need to keep the application running?**  
A: Yes, the SSH tunnel only works while the application is running and connected.

**Q: Can I use multiple USB devices?**  
A: This depends on your USB Redirector configuration. One tunnel can carry multiple USB devices if configured properly.

**Q: Will this work without Radmin VPN?**  
A: Yes! That's the purpose - this replaces Radmin VPN with a direct SSH tunnel.

**Q: Is this free?**  
A: The application is free, but GsmMeta may charge for server access/hosting.

**Q: Can I run multiple instances?**  
A: Generally no - SSH keys and config are shared. Each instance would need separate configuration.

**Q: What if I lose my SSH key?**  
A: Generate a new key pair and provide the new public key to GsmMeta.

---

**Version:** 1.0  
**Last Updated:** January 2026  
**Developer:** GsmMeta
