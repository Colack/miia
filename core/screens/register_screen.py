import tkinter as tk
from tkinter import ttk

class RegisterScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        self.pack(expand=True, fill='both')
        
        self.register_frame = ttk.Frame(self)
        self.register_frame.pack(expand=True, fill='both')
        
        self.register_label = ttk.Label(self.register_frame, text="Register")
        self.register_label.pack()
        
        self.username_label = ttk.Label(self.register_frame, text="Username")
        self.username_label.pack()
        
        self.username_entry = ttk.Entry(self.register_frame)
        self.username_entry.pack()
        
        self.password_label = ttk.Label(self.register_frame, text="Password")
        self.password_label.pack()
        
        self.password_entry = ttk.Entry(self.register_frame, show="*")
        self.password_entry.pack()
        
        self.register_button = ttk.Button(self.register_frame, text="Register", command=self.register)
        self.register_button.pack()
        
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.controller.user_manager.register_user(username, password):
            tk.messagebox.showinfo("Registration Successful", "You have been registered successfully")
        else:
            tk.messagebox.showerror("Registration Failed", "Username already exists")