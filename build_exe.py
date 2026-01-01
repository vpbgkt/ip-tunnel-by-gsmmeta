"""
Build Script for Creating Standalone Executable
Packages the IP Tunnel application into a Windows executable using PyInstaller.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def build_executable():
    """Build standalone executable using PyInstaller."""
    
    print("=" * 60)
    print("IP Tunnel by GsmMeta - Build Script")
    print("=" * 60)
    print()
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller found")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed")
    
    print()
    
    # Build configuration
    app_name = "IP_Tunnel_GsmMeta"
    main_script = "main.py"
    
    # Check for icon files
    icon_file = None
    if Path("logo.png").exists():
        print("✓ Found logo.png, converting to .ico...")
        try:
            from PIL import Image
            img = Image.open("logo.png")
            img.save("logo.ico", format='ICO', sizes=[(256, 256)])
            icon_file = "logo.ico"
            print("✓ Created logo.ico from logo.png")
        except Exception as e:
            print(f"⚠ Could not convert logo.png to .ico: {e}")
            if Path("icon.ico").exists():
                icon_file = "icon.ico"
    elif Path("icon.ico").exists():
        icon_file = "icon.ico"
    
    # PyInstaller command
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--name", app_name,
        "--onefile",  # Single executable file
        "--windowed",  # No console window
        "--clean",
        "--add-data", "logo.png;.",  # Include logo.png in executable
        main_script
    ]
    
    # Add icon if exists
    if icon_file:
        cmd.extend(["--icon", icon_file])
        print(f"✓ Using icon: {icon_file}")
    else:
        print("ℹ No icon file found. Continuing without icon.")
    
    # Add hidden imports for CustomTkinter
    hidden_imports = [
        "customtkinter",
        "PIL._tkinter_finder"
    ]
    
    for module in hidden_imports:
        cmd.extend(["--hidden-import", module])
    
    print()
    print("Building executable...")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    # Run PyInstaller
    try:
        result = subprocess.run(cmd, check=True)
        
        print()
        print("=" * 60)
        print("✓ Build completed successfully!")
        print("=" * 60)
        print()
        print(f"Executable location: dist/{app_name}.exe")
        print()
        print("You can now distribute the executable file.")
        print("Users can run it directly without installing Python or dependencies.")
        print()
        
        # Ask if should clean build files
        response = input("Clean build files (build/, *.spec)? [y/N]: ")
        if response.lower() == 'y':
            clean_build_files()
        
        return True
        
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 60)
        print("✗ Build failed!")
        print("=" * 60)
        print(f"Error: {e}")
        return False


def clean_build_files():
    """Remove build artifacts."""
    print()
    print("Cleaning build files...")
    
    # Directories to remove
    dirs_to_remove = ["build", "__pycache__"]
    
    for dir_name in dirs_to_remove:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"✓ Removed {dir_name}/")
    
    # Files to remove
    spec_files = list(Path(".").glob("*.spec"))
    for spec_file in spec_files:
        spec_file.unlink()
        print(f"✓ Removed {spec_file}")
    
    print("✓ Cleanup complete")


if __name__ == "__main__":
    success = build_executable()
    
    if not success:
        sys.exit(1)
