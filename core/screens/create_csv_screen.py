import tkinter as tk
from tkinter import ttk

class CreateCSVScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
        
    def setup_ui(self):
        self.pack(expand=True, fill='both')
        
        self.create_csv_frame = ttk.Frame(self)
        self.create_csv_frame.pack(expand=True, fill='both')
        
        self.create_csv_label = ttk.Label(self.create_csv_frame, text="Create CSV")
        self.create_csv_label.pack()
        
        self.csv_name_label = ttk.Label(self.create_csv_frame, text="CSV Name")
        self.csv_name_label.pack()
        
        self.csv_name_entry = ttk.Entry(self.create_csv_frame)
        self.csv_name_entry.pack()
        
        self.csv_data_label = ttk.Label(self.create_csv_frame, text="CSV Data")
        self.csv_data_label.pack()
        
        self.csv_data_text = tk.Text(self.create_csv_frame)
        self.csv_data_text.pack()
        
        self.create_csv_button = ttk.Button(self.create_csv_frame, text="Create CSV", command=self.create_csv)
        self.create_csv_button.pack()
        
        self.back_button = ttk.Button(self.create_csv_frame, text="Back", command=self.back)
        self.back_button.pack()
        
    def create_csv(self):
        csv_name = self.csv_name_entry.get()
        csv_data = self.csv_data_text.get("1.0", tk.END)
        self.controller.csv_manager.create_csv(csv_name, csv_data)
        
    def back(self):
        self.controller.show_dashboard_screen()