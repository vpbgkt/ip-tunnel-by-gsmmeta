"""
Test script to verify the application modules work correctly.
Run this before running the main application.
"""

import sys

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing module imports...")
    print()
    
    tests_passed = 0
    tests_failed = 0
    
    # Test standard library
    modules = [
        ("os", "Standard library"),
        ("sys", "Standard library"),
        ("json", "Standard library"),
        ("subprocess", "Standard library"),
        ("threading", "Standard library"),
        ("pathlib", "Standard library"),
    ]
    
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"✓ {module_name:20} - {description}")
            tests_passed += 1
        except ImportError as e:
            print(f"✗ {module_name:20} - FAILED: {e}")
            tests_failed += 1
    
    print()
    
    # Test third-party dependencies
    dependencies = [
        ("customtkinter", "GUI framework"),
        ("PIL", "Image library (Pillow)"),
        ("pyperclip", "Clipboard operations"),
        ("psutil", "Process management"),
    ]
    
    for module_name, description in dependencies:
        try:
            __import__(module_name)
            print(f"✓ {module_name:20} - {description}")
            tests_passed += 1
        except ImportError as e:
            print(f"✗ {module_name:20} - FAILED: {e}")
            tests_failed += 1
    
    print()
    
    # Test application modules
    app_modules = [
        ("ssh_key_manager", "SSH key operations"),
        ("config_manager", "Configuration management"),
        ("connection_manager", "Connection handling"),
    ]
    
    for module_name, description in app_modules:
        try:
            __import__(module_name)
            print(f"✓ {module_name:20} - {description}")
            tests_passed += 1
        except ImportError as e:
            print(f"✗ {module_name:20} - FAILED: {e}")
            tests_failed += 1
    
    print()
    print("=" * 60)
    print(f"Tests passed: {tests_passed}")
    print(f"Tests failed: {tests_failed}")
    print("=" * 60)
    
    return tests_failed == 0


def test_ssh_availability():
    """Test if SSH client is available on the system."""
    import subprocess
    
    print()
    print("Testing SSH client availability...")
    
    try:
        result = subprocess.run(
            ["ssh", "-V"],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        # SSH writes version to stderr
        version_info = result.stderr.strip() or result.stdout.strip()
        
        if version_info:
            print(f"✓ SSH client found: {version_info}")
            return True
        else:
            print("✗ SSH client not responding properly")
            return False
            
    except FileNotFoundError:
        print("✗ SSH client not found!")
        print()
        print("  Windows 10/11: OpenSSH should be built-in")
        print("  If not available, enable it:")
        print("    Settings > Apps > Optional Features > OpenSSH Client")
        print()
        return False
    except Exception as e:
        print(f"✗ Error checking SSH: {e}")
        return False


def test_config_directory():
    """Test if configuration directory can be created."""
    import os
    from pathlib import Path
    
    print()
    print("Testing configuration directory...")
    
    try:
        appdata = os.getenv('APPDATA')
        config_dir = Path(appdata) / "IPTunnelGsmMeta"
        
        # Try to create directory
        config_dir.mkdir(parents=True, exist_ok=True)
        
        if config_dir.exists():
            print(f"✓ Configuration directory: {config_dir}")
            return True
        else:
            print(f"✗ Failed to create: {config_dir}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("IP Tunnel by GsmMeta - System Test")
    print("=" * 60)
    print()
    
    # Run tests
    imports_ok = test_imports()
    ssh_ok = test_ssh_availability()
    config_ok = test_config_directory()
    
    print()
    print("=" * 60)
    
    if imports_ok and ssh_ok and config_ok:
        print("✓ All tests passed!")
        print()
        print("The application is ready to run.")
        print("Execute: python main.py")
        print("=" * 60)
        return 0
    else:
        print("✗ Some tests failed!")
        print()
        print("Please fix the issues above before running the application.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
