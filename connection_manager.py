"""
Connection Manager Module
Manages SSH tunnel connections via PowerShell with status monitoring.
"""

import subprocess
import threading
import time
import psutil
import platform


class ConnectionManager:
    """Manages SSH tunnel connection lifecycle and monitoring."""
    
    def __init__(self, status_callback=None):
        """
        Initialize connection manager.
        
        Args:
            status_callback (callable): Function to call when status changes
                                       Signature: callback(is_connected: bool, message: str)
        """
        self.process = None
        self.is_connected = False
        self.monitor_thread = None
        self.should_monitor = False
        self.status_callback = status_callback
        self.last_error = ""
    
    def connect(self, ssh_command):
        """
        Start SSH tunnel connection.
        
        Args:
            ssh_command (str): Full SSH command to execute
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if self.is_connected:
            return False, "Already connected. Disconnect first."
        
        if not ssh_command or not ssh_command.strip():
            return False, "SSH command is empty"
        
        try:
            # Prepare command for PowerShell execution
            if platform.system() == "Windows":
                # Execute via PowerShell
                powershell_cmd = [
                    "powershell.exe",
                    "-NoProfile",
                    "-NonInteractive",
                    "-Command",
                    ssh_command
                ]
            else:
                # Direct execution for Linux/Mac
                powershell_cmd = ssh_command.split()
            
            # Start the SSH process
            self.process = subprocess.Popen(
                powershell_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            )
            
            # Give it a moment to start
            time.sleep(1)
            
            # Check if process is still running
            if self.process.poll() is not None:
                # Process terminated immediately - likely an error
                stderr = self.process.stderr.read().decode('utf-8', errors='ignore')
                stdout = self.process.stdout.read().decode('utf-8', errors='ignore')
                error_msg = stderr or stdout or "SSH process terminated immediately"
                self.last_error = error_msg
                return False, f"Connection failed: {error_msg}"
            
            # Process started successfully
            self.is_connected = True
            self._notify_status(True, "Connected to server")
            
            # Start monitoring thread
            self.should_monitor = True
            self.monitor_thread = threading.Thread(target=self._monitor_connection, daemon=True)
            self.monitor_thread.start()
            
            return True, "Connected successfully"
            
        except FileNotFoundError:
            error_msg = "PowerShell not found. This should not happen on Windows."
            self.last_error = error_msg
            return False, error_msg
        except Exception as e:
            error_msg = f"Connection error: {str(e)}"
            self.last_error = error_msg
            return False, error_msg
    
    def disconnect(self):
        """
        Terminate SSH tunnel connection.
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.is_connected:
            return False, "Not connected"
        
        try:
            # Stop monitoring
            self.should_monitor = False
            
            # Terminate the process
            if self.process:
                # Try graceful termination first
                self.process.terminate()
                
                # Wait up to 3 seconds for termination
                try:
                    self.process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    # Force kill if termination didn't work
                    self.process.kill()
                    self.process.wait()
                
                self.process = None
            
            self.is_connected = False
            self._notify_status(False, "Disconnected from server")
            
            return True, "Disconnected successfully"
            
        except Exception as e:
            error_msg = f"Disconnect error: {str(e)}"
            self.last_error = error_msg
            self.is_connected = False
            self._notify_status(False, error_msg)
            return False, error_msg
    
    def _monitor_connection(self):
        """
        Monitor connection status in background thread.
        Checks if the SSH process is still running.
        """
        while self.should_monitor and self.is_connected:
            try:
                # Check if process is still alive
                if self.process:
                    poll_result = self.process.poll()
                    
                    if poll_result is not None:
                        # Process has terminated
                        self.is_connected = False
                        
                        # Read error output
                        try:
                            stderr = self.process.stderr.read().decode('utf-8', errors='ignore')
                            stdout = self.process.stdout.read().decode('utf-8', errors='ignore')
                            error_msg = stderr or stdout or "Connection lost"
                            self.last_error = error_msg
                        except:
                            error_msg = "Connection lost"
                            self.last_error = error_msg
                        
                        self._notify_status(False, f"Disconnected: {error_msg}")
                        break
                else:
                    # Process object is None
                    self.is_connected = False
                    self._notify_status(False, "Connection lost")
                    break
                
                # Sleep before next check
                time.sleep(2)
                
            except Exception as e:
                self.is_connected = False
                error_msg = f"Monitor error: {str(e)}"
                self.last_error = error_msg
                self._notify_status(False, error_msg)
                break
    
    def _notify_status(self, is_connected, message):
        """
        Notify status change via callback.
        
        Args:
            is_connected (bool): Current connection status
            message (str): Status message
        """
        if self.status_callback:
            try:
                self.status_callback(is_connected, message)
            except Exception as e:
                print(f"Status callback error: {e}")
    
    def get_status(self):
        """
        Get current connection status.
        
        Returns:
            tuple: (is_connected: bool, message: str)
        """
        if self.is_connected:
            return True, "Connected"
        else:
            return False, self.last_error or "Disconnected"
    
    def is_process_running(self):
        """
        Check if SSH process is running.
        
        Returns:
            bool: True if process is running, False otherwise
        """
        if self.process:
            return self.process.poll() is None
        return False
