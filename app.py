"""
    AutoManager v0.0.1 "Miia"
    (c) 2024 by Jack Spencer

    This is a tkinter program to edit, modify, and udpate CSV tables.
"""

# Importing the necessary modules

import os
import sys
import bcrypt
import json
import csv
import datetime
import time
import logging
import random
import string
import requests
import tkinter as tk
import ttkbootstrap as tb

from tkinter import ttk, messagebox, filedialog, simpledialog
from ttkbootstrap import style
from ttkbootstrap.widgets import Button, Frame, Label, Entry, Combobox, Treeview
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from dotenv import load_dotenv
from screeninfo import get_monitors

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
    # Load environment variables
    load_dotenv()
    
    # Load default theme
    theme = os.getenv("DEFAULT_THEME", "darkly")
    
    # Initialize the application
    root = tb.Window(themename=theme)
    app = application_ui.ApplicationUI(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()