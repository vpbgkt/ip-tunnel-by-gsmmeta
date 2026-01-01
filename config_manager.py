"""
Configuration Manager Module
Handles persistent storage of server connection commands and app settings.
"""

import json
import os
from pathlib import Path


class ConfigManager:
    """Manages application configuration persistence."""
    
    def __init__(self, app_name="IPTunnelGsmMeta"):
        """
        Initialize configuration manager.
        
        Args:
            app_name (str): Application name for config directory
        """
        self.app_name = app_name
        self.config_dir = self._get_config_directory()
        self.config_file = self.config_dir / "config.json"
        self.config_data = self._load_config()
    
    def _get_config_directory(self):
        """
        Get application configuration directory in AppData.
        
        Returns:
            Path: Path to configuration directory
        """
        if os.name == 'nt':  # Windows
            appdata = os.getenv('APPDATA')
            config_dir = Path(appdata) / self.app_name
        else:  # Linux/Mac fallback
            config_dir = Path.home() / f".{self.app_name.lower()}"
        
        # Create directory if it doesn't exist
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir
    
    def _load_config(self):
        """
        Load configuration from file.
        
        Returns:
            dict: Configuration data
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self._get_default_config()
        else:
            return self._get_default_config()
    
    def _get_default_config(self):
        """
        Get default configuration structure.
        
        Returns:
            dict: Default configuration
        """
        return {
            "server_command": "",
            "auto_connect": False,
            "minimize_to_tray": True,
            "show_notifications": True,
            "first_run": True
        }
    
    def save_config(self):
        """
        Save current configuration to file.
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config_data, indent=4, fp=f)
            return True, "Configuration saved successfully"
        except Exception as e:
            return False, f"Error saving configuration: {str(e)}"
    
    def get_server_command(self):
        """
        Get stored server connection command.
        
        Returns:
            str: Server command or empty string
        """
        return self.config_data.get("server_command", "")
    
    def set_server_command(self, command):
        """
        Save server connection command.
        
        Args:
            command (str): SSH tunnel command
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if not command or not command.strip():
            return False, "Command cannot be empty"
        
        # Basic validation - should start with "ssh"
        if not command.strip().startswith("ssh"):
            return False, "Invalid SSH command format"
        
        self.config_data["server_command"] = command.strip()
        self.config_data["first_run"] = False
        return self.save_config()
    
    def is_first_run(self):
        """
        Check if this is the first time running the application.
        
        Returns:
            bool: True if first run, False otherwise
        """
        return self.config_data.get("first_run", True)
    
    def has_server_command(self):
        """
        Check if server command is configured.
        
        Returns:
            bool: True if command exists, False otherwise
        """
        command = self.get_server_command()
        return bool(command and command.strip())
    
    def get_auto_connect(self):
        """Get auto-connect setting."""
        return self.config_data.get("auto_connect", False)
    
    def set_auto_connect(self, enabled):
        """Set auto-connect setting."""
        self.config_data["auto_connect"] = enabled
        return self.save_config()
    
    def get_minimize_to_tray(self):
        """Get minimize to tray setting."""
        return self.config_data.get("minimize_to_tray", True)
    
    def set_minimize_to_tray(self, enabled):
        """Set minimize to tray setting."""
        self.config_data["minimize_to_tray"] = enabled
        return self.save_config()
    
    def clear_configuration(self):
        """
        Clear all configuration and reset to defaults.
        
        Returns:
            tuple: (success: bool, message: str)
        """
        self.config_data = self._get_default_config()
        return self.save_config()
    
    def export_config(self, file_path):
        """
        Export configuration to a file.
        
        Args:
            file_path (str): Path to export file
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            with open(file_path, 'w') as f:
                json.dump(self.config_data, indent=4, fp=f)
            return True, f"Configuration exported to {file_path}"
        except Exception as e:
            return False, f"Export failed: {str(e)}"
    
    def import_config(self, file_path):
        """
        Import configuration from a file.
        
        Args:
            file_path (str): Path to import file
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            with open(file_path, 'r') as f:
                imported_data = json.load(f)
            
            # Validate imported data
            if not isinstance(imported_data, dict):
                return False, "Invalid configuration file format"
            
            self.config_data = imported_data
            return self.save_config()
        except Exception as e:
            return False, f"Import failed: {str(e)}"
