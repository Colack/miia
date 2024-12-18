import tkinter as tk
from tkinter import ttk

class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        self.pack(expand=True, fill='both')
        
        self.login_frame = ttk.Frame(self)
        self.login_frame.pack(expand=True, fill='both')
        
        self.login_label = ttk.Label(self.login_frame, text="Login")
        self.login_label.pack()
        
        self.username_label = ttk.Label(self.login_frame, text="Username")
        self.username_label.pack()
        
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.pack()
        
        self.password_label = ttk.Label(self.login_frame, text="Password")
        self.password_label.pack()
        
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.pack()
        
        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack()
        
        self.register_button = ttk.Button(self.login_frame, text="Register", command=self.register)
        self.register_button.pack()
        
    def login(self):
        from .dashboard_screen import DashboardScreen  # Deferred import to avoid circular import
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.controller.user_manager.login_user(username, password):
            self.controller.show_screen(DashboardScreen(self.master, self.controller))
        else:
            tk.messagebox.showerror("Login Failed", "Invalid username or password")
            
    def register(self):
        from .register_screen import RegisterScreen
        self.controller.show_screen(RegisterScreen(self.master, self.controller))