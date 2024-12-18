import tkinter as tk
from tkinter import ttk

from .login_screen import LoginScreen
from .create_csv_screen import CreateCSVScreen
from .read_csv_screen import ReadCSVScreen
from .update_csv_screen import UpdateCSVScreen
from .delete_csv_screen import DeleteCSVScreen

class DashboardScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
        
    def setup_ui(self):
        self.pack(expand=True, fill='both')
        
        self.dashboard_frame = ttk.Frame(self)
        self.dashboard_frame.pack(expand=True, fill='both')
        
        self.dashboard_label = ttk.Label(self.dashboard_frame, text="Dashboard")
        self.dashboard_label.pack()
        
        # Menus: CSV CRUD Operations, User Management, Logout
        
        # CSV CRUD Operations
        self.csv_crud_label = ttk.Label(self.dashboard_frame, text="CSV CRUD Operations")
        self.csv_crud_label.pack()
        
        self.csv_crud_frame = ttk.Frame(self.dashboard_frame)
        self.csv_crud_frame.pack()
        
        self.create_csv_button = ttk.Button(self.csv_crud_frame, text="Create CSV", command=self.create_csv)
        self.create_csv_button.pack(side='left')
        
        self.read_csv_button = ttk.Button(self.csv_crud_frame, text="Read CSV", command=self.read_csv)
        self.read_csv_button.pack(side='left')
        
        self.update_csv_button = ttk.Button(self.csv_crud_frame, text="Update CSV", command=self.update_csv)
        self.update_csv_button.pack(side='left')
        
        self.delete_csv_button = ttk.Button(self.csv_crud_frame, text="Delete CSV", command=self.delete_csv)
        self.delete_csv_button.pack(side='left')
        
        self.logout_button = ttk.Button(self.dashboard_frame, text="Logout", command=self.logout)
        self.logout_button.pack()
        
    def logout(self):
        self.controller.user_manager.logout()
        self.controller.show_screen(LoginScreen(self.master, self.controller))
        
    def create_csv(self):
        self.controller.show_screen(CreateCSVScreen(self.master, self.controller))
        
    def read_csv(self):
        self.controller.show_screen(ReadCSVScreen(self.master, self.controller))
        
    def update_csv(self):
        self.controller.show_screen(UpdateCSVScreen(self.master, self.controller))
        
    def delete_csv(self):
        self.controller.show_screen(DeleteCSVScreen(self.master, self.controller))