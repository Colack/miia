import tkinter as tk
from tkinter import ttk, messagebox
from core.file_manager import FileManager
from core.auth import AuthManager
from core.order_manager import read_orders, save_orders
from core.backup import backup_to_google_drive

class AutoShopApp:
    def __init__(self, root, debug_mode):
        self.root = root
        self.debug_mode = debug_mode
        self.file_manager = FileManager()
        self.orders = []
        self.current_csv = None
        self.setup_ui()

    def setup_ui(self):
        """Set up the UI."""
        self.root.title("AutoShop Manager - CSV Management")
        
        # Select CSV File Section
        file_frame = ttk.LabelFrame(self.root, text="CSV File Management")
        file_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(file_frame, text="Select CSV File:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.csv_var = tk.StringVar()
        self.csv_dropdown = ttk.Combobox(file_frame, textvariable=self.csv_var, state="readonly")
        self.csv_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.load_csv_files()

        ttk.Button(file_frame, text="Load", command=self.load_csv).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(file_frame, text="Create New CSV", command=self.show_create_csv).grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # Orders Table
        self.table_frame = ttk.LabelFrame(self.root, text="Orders")
        self.table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.tree = ttk.Treeview(self.table_frame, columns=("Order ID", "Customer", "Vehicle"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

    def load_csv_files(self):
        """Load available CSV files into the dropdown."""
        files = self.file_manager.list_csv_files()
        self.csv_dropdown["values"] = list(files.keys())

    def load_csv(self):
        """Load the selected CSV file."""
        file_name = self.csv_var.get()
        if not file_name:
            messagebox.showerror("Error", "Please select a CSV file.")
            return
        self.current_csv = file_name
        self.orders = self.file_manager.read_csv(file_name)
        self.populate_table()

    def populate_table(self):
        """Populate the orders table."""
        self.tree.delete(*self.tree.get_children())
        for order in self.orders:
            self.tree.insert("", "end", values=(order['order_id'], order['customer_name'], order['vehicle_model']))

    def show_create_csv(self):
        """Show the UI to create a new CSV file."""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Create New CSV File")
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        ttk.Label(frame, text="CSV File Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.new_csv_name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.new_csv_name_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Fields (comma-separated):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.new_csv_fields_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.new_csv_fields_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Create", command=self.create_csv).grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        ttk.Button(frame, text="Back", command=self.setup_ui).grid(row=2, column=0, sticky="ew", padx=5, pady=5)

    def create_csv(self):
        """Create a new CSV file."""
        name = self.new_csv_name_var.get()
        fields = [field.strip() for field in self.new_csv_fields_var.get().split(",") if field.strip()]
        if not name or not fields:
            messagebox.showerror("Error", "Both file name and fields are required.")
            return
        try:
            self.file_manager.create_csv(name, fields)
            messagebox.showinfo("Success", f"CSV file '{name}' created.")
            self.setup_ui()
            self.load_csv_files()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
