import tkinter as tk
from tkinter import ttk, messagebox
from core.order_manager import read_orders, save_orders
from core.backup import backup_to_google_drive

class AutoShopApp:
    def __init__(self, root, csv_file, debug_mode):
        self.root = root
        self.csv_file = csv_file
        self.debug_mode = debug_mode
        self.orders = []
        self.setup_ui()
        self.read_orders()

    def setup_ui(self):
        self.root.title("AutoShop Manager")

        # UI Components
        form_frame = ttk.LabelFrame(self.root, text="Order Details")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(form_frame, text="Customer Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.customer_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.customer_name_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Contact (Phone/Email):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.contact_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.contact_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Vehicle Model:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.vehicle_model_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.vehicle_model_var).grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        ttk.Button(form_frame, text="Backup", command=self.backup_to_drive).grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        # Table
        table_frame = ttk.LabelFrame(self.root, text="Orders")
        table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.tree = ttk.Treeview(table_frame, columns=("Order ID", "Customer", "Vehicle"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

    def read_orders(self):
        self.orders = read_orders(self.csv_file)
        self.tree.delete(*self.tree.get_children())
        for order in self.orders:
            self.tree.insert("", "end", values=(order['order_id'], order['customer_name'], order['vehicle_model']))

    def backup_to_drive(self):
        backup_to_google_drive(self.csv_file)
