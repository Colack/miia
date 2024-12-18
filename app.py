"""
    AutoManager v0.0.1 "Miia"
    (c) 2024 by Jack Spencer

    This is a tkinter program to edit, modify, and update CSV tables.
"""

# Importing the necessary modules

import os
import json
import logging
import tkinter as tk
import ttkbootstrap as tb

from dotenv import load_dotenv

# Local Imports

from core import file_manager, user_manager, application_ui

# Global Variables

debug_mode = False
version = "0.0.1"

# Debug mode uses the logging module to output debug messages
if debug_mode:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
else:
    logging.basicConfig(level=logging.WARNING)

def main():
    """
    The main function initializes the application.
    It loads environment variables, sets the theme, and starts the main application loop.
    """
    # Load environment variables
    load_dotenv()
    
    # Load default theme from environment variables or use "darkly" as default
    theme = os.getenv("DEFAULT_THEME", "darkly")
    
    # Initialize the application window with the specified theme
    root = tb.Window(themename=theme)
    
    # Create an instance of the ApplicationUI class
    app = application_ui.ApplicationUI(root, debug_mode, "AutoManager", version)
    
    # Start the Tkinter main loop
    root.mainloop()
    
if __name__ == "__main__":
    main()