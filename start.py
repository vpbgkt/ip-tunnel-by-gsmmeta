"""
Quick Start Guide for IP Tunnel by GsmMeta
"""

print("=" * 60)
print("IP Tunnel by GsmMeta - Quick Start")
print("=" * 60)
print()
print("This application helps you create SSH tunnels for USB sharing.")
print()
print("To run the application:")
print()
print("1. Install dependencies:")
print("   pip install -r requirements.txt")
print()
print("2. Run the application:")
print("   python main.py")
print()
print("3. (Optional) Build standalone executable:")
print("   python build_exe.py")
print()
print("=" * 60)
print()

# Check if dependencies are installed
import sys

try:
    import customtkinter
    print("✓ customtkinter is installed")
except ImportError:
    print("✗ customtkinter is NOT installed")
    print("  Run: pip install -r requirements.txt")
    sys.exit(1)

try:
    import pyperclip
    print("✓ pyperclip is installed")
except ImportError:
    print("✗ pyperclip is NOT installed")
    print("  Run: pip install -r requirements.txt")
    sys.exit(1)

try:
    import psutil
    print("✓ psutil is installed")
except ImportError:
    print("✗ psutil is NOT installed")
    print("  Run: pip install -r requirements.txt")
    sys.exit(1)

try:
    from PIL import Image
    print("✓ Pillow is installed")
except ImportError:
    print("✗ Pillow is NOT installed")
    print("  Run: pip install -r requirements.txt")
    sys.exit(1)

print()
print("All dependencies are installed!")
print()
print("You can now run the application with:")
print("   python main.py")
print()
