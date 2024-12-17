import os
import platform
import subprocess

def build():
    """Run PyInstaller to bundle the application."""
    command = [
        "pyinstaller",
        "--onefile",
        "--name", "AutoShopManager",
        "main.py"
    ]
    subprocess.run(command)

def main():
    system = platform.system()
    print(f"Building for {system}...")
    build()
    print("Build complete. Executable is located in the 'dist/' directory.")

if __name__ == "__main__":
    main()
