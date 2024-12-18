import tkinter as tk
import ttkbootstrap as tb
from tkinter import ttk, messagebox
from core.file_manager import FileManager
from core.user_manager import UserManager
from core.csv_manager import CSVManager
import logging

from .ui_util import *

from .screens.login_screen import LoginScreen

# Application UI Class
class ApplicationUI:
    def __init__(self, root, debug_mode, title, version):
        self.title = title
        self.version = version
        self.root = root
        self.debug_mode = debug_mode
        self.file_manager = FileManager()
        self.user_manager = UserManager()
        self.csv_manager = CSVManager()
        self.current_screen = None
        self.setup_ui()
        
    def setup_ui(self):
        set_title(self.root, self.title + " v" + self.version)
        set_dimensions(self.root, get_screen_width(), get_screen_height())
        center_window(self.root)
        
        self.root.resizable(False, False)
        self.root.style.theme_use("darkly")
        
        set_window_binding(self.root, "<Control-q>", self.quit_app)
        
        self.show_screen(LoginScreen(self.root, self))
        
    def quit_app(self, event):
        self.root.quit()
        
    def show_screen(self, screen):
        if self.current_screen:
            self.current_screen.pack_forget()
        self.current_screen = screen
        self.current_screen.pack(expand=True, fill='both')