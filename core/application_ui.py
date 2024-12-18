import tkinter as tk
import ttkbootstrap as tb
from tkinter import ttk, messagebox
from core.file_manager import FileManager
from core.user_manager import UserManager
import logging

class ApplicationUI:
    def __init__(self, root, debug_mode):
        self.root = root
        self.debug_mode = debug_mode
        self.file_manager = FileManager()
        self.user_manager = UserManager()
        self.current_screen = None
        self.setup_ui()
        
    