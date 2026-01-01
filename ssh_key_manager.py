"""
SSH Key Manager Module
Handles SSH key generation, detection, and public key retrieval.
"""

import os
import subprocess
import platform
from pathlib import Path


class SSHKeyManager:
    """Manages SSH key operations including generation and retrieval."""
    
    def __init__(self):
        """Initialize SSH key manager with default paths."""
        self.home_dir = Path.home()
        self.ssh_dir = self.home_dir / ".ssh"
        self.private_key_path = self.ssh_dir / "id_rsa"
        self.public_key_path = self.ssh_dir / "id_rsa.pub"
    
    def check_ssh_keys_exist(self):
        """
        Check if SSH key pair already exists.
        
        Returns:
            bool: True if both private and public keys exist, False otherwise
        """
        return self.private_key_path.exists() and self.public_key_path.exists()
    
    def generate_ssh_key(self, email="", key_type="rsa", bits=2048):
        """
        Generate a new SSH key pair using ssh-keygen.
        
        Args:
            email (str): Optional email/comment for the key
            key_type (str): Type of key to generate (rsa, ed25519, etc.)
            bits (int): Number of bits for RSA keys
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Create .ssh directory if it doesn't exist
            self.ssh_dir.mkdir(parents=True, exist_ok=True)
            
            # Build ssh-keygen command
            cmd = [
                "ssh-keygen",
                "-t", key_type,
                "-b", str(bits),
                "-f", str(self.private_key_path),
                "-N", "",  # No passphrase
            ]
            
            if email:
                cmd.extend(["-C", email])
            
            # Execute ssh-keygen
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            )
            
            if result.returncode == 0:
                return True, "SSH key pair generated successfully!"
            else:
                error_msg = result.stderr.strip() or result.stdout.strip()
                return False, f"Error generating SSH key: {error_msg}"
                
        except FileNotFoundError:
            return False, "SSH client not found. Please install OpenSSH for Windows."
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def get_public_key(self):
        """
        Read and return the SSH public key content.
        
        Returns:
            tuple: (success: bool, key_content: str or error_message: str)
        """
        try:
            if not self.public_key_path.exists():
                return False, "Public key file not found. Please generate SSH keys first."
            
            with open(self.public_key_path, 'r') as f:
                public_key = f.read().strip()
            
            return True, public_key
            
        except Exception as e:
            return False, f"Error reading public key: {str(e)}"
    
    def get_private_key_path(self):
        """
        Get the absolute path to the private key file.
        
        Returns:
            str: Absolute path to private key
        """
        return str(self.private_key_path.absolute())
    
    def delete_existing_keys(self):
        """
        Delete existing SSH key pair (use with caution).
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            deleted = []
            
            if self.private_key_path.exists():
                self.private_key_path.unlink()
                deleted.append("private key")
            
            if self.public_key_path.exists():
                self.public_key_path.unlink()
                deleted.append("public key")
            
            if deleted:
                return True, f"Deleted: {', '.join(deleted)}"
            else:
                return True, "No keys to delete"
                
        except Exception as e:
            return False, f"Error deleting keys: {str(e)}"
