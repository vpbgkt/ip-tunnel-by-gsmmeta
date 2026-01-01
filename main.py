"""
IP Tunnel by GsmMeta
Main GUI Application

A Windows desktop application for managing SSH tunnels for USB port sharing.
"""

import customtkinter as ctk
import pyperclip
import threading
from tkinter import messagebox
from ssh_key_manager import SSHKeyManager
from config_manager import ConfigManager
from connection_manager import ConnectionManager


# Set appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class IPTunnelApp(ctk.CTk):
    """Main application window."""
    
    def __init__(self):
        """Initialize the application."""
        super().__init__()
        
        # Window configuration
        self.title("IP Tunnel by GsmMeta.com")
        self.geometry("320x200")
        self.resizable(False, False)
        
        # Set window icon
        self.set_window_icon()
        
        # Center window on screen
        self.center_window()
        
        # Initialize managers
        self.ssh_manager = SSHKeyManager()
        self.config_manager = ConfigManager()
        self.connection_manager = ConnectionManager(status_callback=self.on_connection_status_changed)
        
        # UI state
        self.current_view = None
        
        # Create main container
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load appropriate view
        self.load_view()
        
        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Center the window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def set_window_icon(self):
        """Set window icon from logo.png if it exists."""
        try:
            import os
            from PIL import Image
            
            logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
            if os.path.exists(logo_path):
                # Set window icon
                icon_image = Image.open(logo_path)
                self.iconphoto(True, ctk.CTkImage(light_image=icon_image, size=(32, 32))._light_image)
        except Exception as e:
            # Silently fail if icon cannot be set
            pass
    
    def load_view(self):
        """Load appropriate view based on configuration state."""
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Check if server command is configured
        if self.config_manager.has_server_command():
            self.show_connection_view()
        else:
            self.show_setup_view()
    
    def show_setup_view(self):
        """Show initial setup view for SSH key generation and server configuration."""
        self.current_view = "setup"
        
        # Resize window for setup view
        self.geometry("600x600")
        
        # Create scrollable frame for content
        scrollable_frame = ctk.CTkScrollableFrame(self.main_frame)
        scrollable_frame.pack(fill="both", expand=True)
        
        # Title
        title = ctk.CTkLabel(
            scrollable_frame,
            text="IP Tunnel Setup - GsmMeta.com",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=15)
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            scrollable_frame,
            text="USB Sharing via SSH Tunnel",
            font=("Arial", 13)
        )
        subtitle.pack(pady=(0, 15))
        
        # SSH Key Section
        key_frame = ctk.CTkFrame(scrollable_frame)
        key_frame.pack(fill="x", padx=20, pady=10)
        
        key_title = ctk.CTkLabel(
            key_frame,
            text="Step 1: Generate SSH Public Key",
            font=("Arial", 16, "bold")
        )
        key_title.pack(pady=15)
        
        # Check if keys already exist
        if self.ssh_manager.check_ssh_keys_exist():
            key_status = ctk.CTkLabel(
                key_frame,
                text="✓ SSH keys already exist",
                font=("Arial", 12),
                text_color="green"
            )
            key_status.pack(pady=5)
        
        key_buttons_frame = ctk.CTkFrame(key_frame, fg_color="transparent")
        key_buttons_frame.pack(pady=10)
        
        generate_btn = ctk.CTkButton(
            key_buttons_frame,
            text="Generate SSH Key",
            command=self.generate_ssh_key,
            width=180,
            height=40
        )
        generate_btn.pack(side="left", padx=5)
        
        copy_btn = ctk.CTkButton(
            key_buttons_frame,
            text="Copy Public Key",
            command=self.copy_public_key,
            width=180,
            height=40
        )
        copy_btn.pack(side="left", padx=5)
        
        # Instructions
        instructions = ctk.CTkLabel(
            key_frame,
            text="Generate your SSH key and copy the public key.\nProvide it to GsmMeta.com to receive your server connection command.",
            font=("Arial", 11),
            text_color="gray"
        )
        instructions.pack(pady=10)
        
        # Server Command Section
        server_frame = ctk.CTkFrame(scrollable_frame)
        server_frame.pack(fill="x", padx=20, pady=10)
        
        server_title = ctk.CTkLabel(
            server_frame,
            text="Step 2: Enter Server Connection Command",
            font=("Arial", 16, "bold")
        )
        server_title.pack(pady=15)
        
        server_label = ctk.CTkLabel(
            server_frame,
            text="Paste the SSH tunnel command provided by GsmMeta.com:",
            font=("Arial", 12)
        )
        server_label.pack(pady=5)
        
        self.server_command_text = ctk.CTkTextbox(
            server_frame,
            height=80,
            font=("Consolas", 11)
        )
        self.server_command_text.pack(fill="x", padx=20, pady=10)
        
        save_btn = ctk.CTkButton(
            server_frame,
            text="Save Configuration & Continue",
            command=self.save_server_command,
            width=250,
            height=40,
            font=("Arial", 13, "bold")
        )
        save_btn.pack(pady=15)
        
        # Footer with clickable link
        footer_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        footer_frame.pack(pady=10)
        
        footer = ctk.CTkLabel(
            footer_frame,
            text="For support, visit: ",
            font=("Arial", 10),
            text_color="gray"
        )
        footer.pack(side="left")
        
        link = ctk.CTkLabel(
            footer_frame,
            text="www.GsmMeta.com",
            font=("Arial", 10, "underline"),
            text_color="#1E90FF",
            cursor="hand2"
        )
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: self.open_website("https://www.GsmMeta.com"))
    
    def show_connection_view(self):
        """Show connection control view for established configurations."""
        self.current_view = "connection"
        
        # Resize window for connection view (compact)
        self.geometry("320x200")
        
        # Status indicator (compact)
        self.status_indicator = ctk.CTkLabel(
            self.main_frame,
            text="●",
            font=("Arial", 45),
            text_color="red"
        )
        self.status_indicator.pack(pady=(5, 0))
        
        self.status_text = ctk.CTkLabel(
            self.main_frame,
            text="Disconnected",
            font=("Arial", 10)
        )
        self.status_text.pack(pady=(0, 8))
        
        # Single toggle button
        self.toggle_btn = ctk.CTkButton(
            self.main_frame,
            text="Connect to Server",
            command=self.toggle_connection,
            width=260,
            height=35,
            font=("Arial", 12, "bold"),
            fg_color="green",
            hover_color="darkgreen"
        )
        self.toggle_btn.pack(pady=5)
        
        # Settings button (smaller, bottom)
        settings_btn = ctk.CTkButton(
            self.main_frame,
            text="⚙ Settings",
            command=self.show_settings,
            width=90,
            height=22,
            font=("Arial", 9)
        )
        settings_btn.pack(pady=(10, 5))
        
        # Check if should auto-connect
        if self.config_manager.get_auto_connect():
            self.after(1000, self.toggle_connection)
    
    def generate_ssh_key(self):
        """Generate SSH key pair."""
        # Check if keys exist
        if self.ssh_manager.check_ssh_keys_exist():
            response = messagebox.askyesno(
                "Existing Keys Found",
                "SSH keys already exist. Do you want to regenerate them?\n\nWarning: This will overwrite existing keys."
            )
            if not response:
                return
            
            # Delete existing keys
            success, msg = self.ssh_manager.delete_existing_keys()
            if not success:
                messagebox.showerror("Error", msg)
                return
        
        # Generate new keys
        success, message = self.ssh_manager.generate_ssh_key()
        
        if success:
            messagebox.showinfo("Success", message)
            self.load_view()  # Refresh view to show key exists
        else:
            messagebox.showerror("Error", message)
    
    def copy_public_key(self):
        """Copy SSH public key to clipboard."""
        success, content = self.ssh_manager.get_public_key()
        
        if success:
            try:
                pyperclip.copy(content)
                messagebox.showinfo(
                    "Public Key Copied",
                    "Your SSH public key has been copied to clipboard!\n\n"
                    "Please provide this key to GsmMeta.com support to receive\n"
                    "your server connection command."
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy to clipboard: {str(e)}")
        else:
            messagebox.showerror("Error", content)
    
    def save_server_command(self):
        """Save server connection command from text box."""
        command = self.server_command_text.get("1.0", "end-1c").strip()
        
        if not command:
            messagebox.showwarning("Empty Command", "Please enter the server connection command.")
            return
        
        success, message = self.config_manager.set_server_command(command)
        
        if success:
            messagebox.showinfo("Success", "Server command saved successfully!")
            self.load_view()  # Switch to connection view
        else:
            messagebox.showerror("Error", message)
    
    def start_connection(self):
        """Start SSH tunnel connection."""
        command = self.config_manager.get_server_command()
        
        # Disable connect button
        self.connect_btn.configure(state="disabled", text="Connecting...")
        self.status_text.configure(text="Connecting...")
        
        # Run connection in separate thread to avoid blocking UI
        def connect_thread():
            success, message = self.connection_manager.connect(command)
            
            # Update UI in main thread
            self.after(0, lambda: self.on_connection_result(success, message))
        
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def on_connection_result(self, success, message):
        """Handle connection attempt result."""
        if success:
            self.connect_btn.configure(state="disabled")
            self.disconnect_btn.configure(state="normal")
        else:
            self.connect_btn.configure(state="normal", text="Connect to Server")
            messagebox.showerror("Connection Failed", message)
    
    def stop_connection(self):
        """Stop SSH tunnel connection."""
        success, message = self.connection_manager.disconnect()
        
        if success:
            self.connect_btn.configure(state="normal", text="Connect to Server")
            self.disconnect_btn.configure(state="disabled")
        else:
            messagebox.showerror("Disconnect Error", message)
    
    def on_connection_status_changed(self, is_connected, message):
        """
        Callback when connection status changes.
        
        Args:
            is_connected (bool): Current connection status
            message (str): Status message
        """
        def update_ui():
            if is_connected:
                self.status_indicator.configure(text_color="green")
                self.status_text.configure(text="Connected")
                self.connect_btn.configure(state="disabled")
                self.disconnect_btn.configure(state="normal")
            else:
                self.status_indicator.configure(text_color="red")
                self.status_text.configure(text="Disconnected")
                self.connect_btn.configure(state="normal", text="Connect to Server")
                self.disconnect_btn.configure(state="disabled")
    
    def toggle_connection(self):
        """Toggle connection on/off."""
        if self.connection_manager.is_connected:
            # Disconnect
            self.toggle_btn.configure(state="disabled", text="Disconnecting...")
            
            def disconnect_thread():
                success, message = self.connection_manager.disconnect()
                self.after(0, lambda: self.on_disconnect_result(success, message))
            
            threading.Thread(target=disconnect_thread, daemon=True).start()
        else:
            # Connect
            command = self.config_manager.get_server_command()
            self.toggle_btn.configure(state="disabled", text="Connecting...")
            self.status_text.configure(text="Connecting...")
            
            def connect_thread():
                success, message = self.connection_manager.connect(command)
                self.after(0, lambda: self.on_connect_result(success, message))
            
            threading.Thread(target=connect_thread, daemon=True).start()
    
    def on_connect_result(self, success, message):
        """Handle connection attempt result."""
        if success:
            self.toggle_btn.configure(
                state="normal",
                text="Disconnect from Server",
                fg_color="red",
                hover_color="darkred"
            )
        else:
            self.toggle_btn.configure(
                state="normal",
                text="Connect to Server",
                fg_color="green",
                hover_color="darkgreen"
            )
            messagebox.showerror("Connection Failed", message)
    
    def on_disconnect_result(self, success, message):
        """Handle disconnect result."""
        self.toggle_btn.configure(
            state="normal",
            text="Connect to Server",
            fg_color="green",
            hover_color="darkgreen"
        )
        if not success:
            messagebox.showerror("Disconnect Error", message)
    
    def on_connection_status_changed(self, is_connected, message):
        """
        Callback when connection status changes.
        
        Args:
            is_connected (bool): Current connection status
            message (str): Status message
        """
        def update_ui():
            if is_connected:
                self.status_indicator.configure(text_color="green")
                self.status_text.configure(text="Connected")
                self.toggle_btn.configure(
                    state="normal",
                    text="Disconnect from Server",
                    fg_color="red",
                    hover_color="darkred"
                )
            else:
                self.status_indicator.configure(text_color="red")
                self.status_text.configure(text="Disconnected")
                self.toggle_btn.configure(
                    state="normal",
                    text="Connect to Server",
                    fg_color="green",
                    hover_color="darkgreen"
                )
        
        # Update UI in main thread
        self.after(0, update_ui)
    
    def show_settings(self):
        """Show settings dialog."""
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("500x400")
        settings_window.resizable(False, False)
        
        # Make modal
        settings_window.transient(self)
        settings_window.grab_set()
        
        # Title
        title = ctk.CTkLabel(
            settings_window,
            text="Settings",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=20)
        
        # Auto-connect setting
        auto_connect_var = ctk.BooleanVar(value=self.config_manager.get_auto_connect())
        auto_connect_check = ctk.CTkCheckBox(
            settings_window,
            text="Auto-connect on startup",
            variable=auto_connect_var,
            font=("Arial", 12)
        )
        auto_connect_check.pack(pady=10)
        
        # Server command section
        command_frame = ctk.CTkFrame(settings_window)
        command_frame.pack(fill="x", padx=20, pady=20)
        
        command_label = ctk.CTkLabel(
            command_frame,
            text="Server Connection Command:",
            font=("Arial", 12, "bold")
        )
        command_label.pack(pady=5)
        
        command_text = ctk.CTkTextbox(
            command_frame,
            height=80,
            font=("Consolas", 10)
        )
        command_text.pack(fill="x", padx=10, pady=5)
        command_text.insert("1.0", self.config_manager.get_server_command())
        
        # Buttons
        button_frame = ctk.CTkFrame(settings_window, fg_color="transparent")
        button_frame.pack(pady=20)
        
        def save_settings():
            # Save auto-connect
            self.config_manager.set_auto_connect(auto_connect_var.get())
            
            # Save command
            new_command = command_text.get("1.0", "end-1c").strip()
            if new_command != self.config_manager.get_server_command():
                success, msg = self.config_manager.set_server_command(new_command)
                if not success:
                    messagebox.showerror("Error", msg)
                    return
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            settings_window.destroy()
            self.load_view()  # Refresh view
        
        def reset_config():
            response = messagebox.askyesno(
                "Reset Configuration",
                "This will clear all settings and return to setup.\n\nAre you sure?"
            )
            if response:
                # Disconnect if connected
                if self.connection_manager.is_connected:
                    self.connection_manager.disconnect()
                
                self.config_manager.clear_configuration()
                messagebox.showinfo("Reset Complete", "Configuration has been reset.")
                settings_window.destroy()
                self.load_view()
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save Settings",
            command=save_settings,
            width=140,
            height=35
        )
        save_btn.pack(side="left", padx=5)
        
        reset_btn = ctk.CTkButton(
            button_frame,
            text="Reset Configuration",
            command=reset_config,
            width=140,
            height=35,
            fg_color="orange",
            hover_color="darkorange"
        )
        reset_btn.pack(side="left", padx=5)
        
        close_btn = ctk.CTkButton(
            button_frame,
            text="Close",
            command=settings_window.destroy,
            width=140,
            height=35
        )
        close_btn.pack(side="left", padx=5)
    
    def open_website(self, url):
        """Open website in default browser."""
        import webbrowser
        webbrowser.open(url)
    
    def on_closing(self):
        """Handle window close event."""
        # Disconnect if connected
        if self.connection_manager.is_connected:
            response = messagebox.askyesno(
                "Disconnect?",
                "You are currently connected. Disconnect and exit?"
            )
            if response:
                self.connection_manager.disconnect()
                self.destroy()
        else:
            self.destroy()


def main():
    """Main entry point."""
    app = IPTunnelApp()
    app.mainloop()


if __name__ == "__main__":
    main()
