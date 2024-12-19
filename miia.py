#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import pyautogui
import os
import sys
from datetime import datetime

class CSVViewScreen(tk.Frame):
    def __init__(self, parent, app, file_path):
        super().__init__(parent)
        self.app = app
        self.file_path = file_path

        # Auto-generate CSV file if it doesn't exist
        if not os.path.exists(self.file_path):
            self.generate_default_csv()

        self.df = pd.DataFrame()
        self.setup_ui()

    def setup_ui(self):
        # Dark mode for the GUI
        self.configure(bg="black")

        title_label = tk.Label(self, text="Miia", fg="white", bg="black", font=("Arial", 16))
        title_label.pack(pady=10)

        # Search bar
        search_frame = tk.Frame(self, bg="black")
        search_frame.pack(pady=5)
        search_label = tk.Label(search_frame, text="Search:", fg="white", bg="black")
        search_label.pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        search_button = tk.Button(search_frame, text="Search", command=self.search, bg="gray", fg="white")
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Light mode styling for the Treeview
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        fieldbackground="white")

        self.tree = ttk.Treeview(self, show='headings')
        self.tree.pack(expand=True, fill='both', pady=10, padx=10)
        self.tree.bind('<Double-1>', self.on_double_click)  # Bind double-click for inline editing

        # Load CSV data
        self.load_csv()

        # Buttons for row management
        button_frame = tk.Frame(self, bg="black")
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, text="Add", command=self.add_row, bg="gray", fg="white")
        add_button.pack(side=tk.LEFT, padx=5)

        edit_button = tk.Button(button_frame, text="Edit", command=self.edit_row, bg="gray", fg="white")
        edit_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(button_frame, text="Delete", command=self.delete_row, bg="gray", fg="white")
        delete_button.pack(side=tk.LEFT, padx=5)

    def generate_default_csv(self):
        columns = [
            "name", "contact", "address", "location", "car_model", "car_year", "car_color",
            "operation", "price", "discount", "notes", "created_at", "updated_at", "is_completed"
        ]

        default_data = [
            [
                "John Doe", "1234567890", "123 Elm St", "NY", "Toyota Corolla", "2015", "Red",
                "Oil Change", "50", "5", "N/A", datetime.now().isoformat(), datetime.now().isoformat(), "False"
            ],
            [
                "Jane Smith", "0987654321", "456 Oak St", "LA", "Honda Civic", "2018", "Blue",
                "Tire Rotation", "40", "0", "Customer requested premium tires.", datetime.now().isoformat(), datetime.now().isoformat(), "True"
            ]
        ]

        df = pd.DataFrame(default_data, columns=columns)
        df.index += 1  # Start index from 1 for id consistency
        df.to_csv(self.file_path, index_label="id")

    def load_csv(self):
        try:
            self.df = pd.read_csv(self.file_path, index_col="id")

            # Convert price and discount to numeric types
            self.df["price"] = pd.to_numeric(self.df["price"], errors="coerce")
            self.df["discount"] = pd.to_numeric(self.df["discount"], errors="coerce")

            # Parse created_at and updated_at as datetime
            self.df["created_at"] = pd.to_datetime(self.df["created_at"], errors="coerce")
            self.df["updated_at"] = pd.to_datetime(self.df["updated_at"], errors="coerce")

            self.render_table()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file: {e}")

    def render_table(self, df=None):
        # Clear existing data in the Treeview
        self.tree.delete(*self.tree.get_children())

        if df is None:
            df = self.df

        # Set up columns and headers
        self.tree["columns"] = list(df.columns)
        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Populate rows
        for index, row in df.iterrows():
            self.tree.insert("", "end", iid=index, values=list(row))  # Use index as iid

    def add_row(self):
        self.show_edit_popup(action="add")

    def edit_row(self):
        selected_item = self.tree.selection()
        if not selected_item:
            pyautogui.alert("No row selected.", "Error")
            return

        row_values = self.tree.item(selected_item[0], "values")
        self.show_edit_popup(action="edit", row_values=row_values)

    def delete_row(self):
        selected_item = self.tree.selection()
        if not selected_item:
            pyautogui.alert("No row selected.", "Error")
            return

        item_id = int(self.tree.selection()[0])
        self.df = self.df.drop(item_id)
        self.df.to_csv(self.file_path, index_label="id")
        self.render_table()

    def show_edit_popup(self, action, row_values=None):
        popup = tk.Toplevel(self)
        popup.title("Edit Row")
        popup.configure(bg="black")

        entry_widgets = []
        for i, column in enumerate(self.df.columns):
            label = tk.Label(popup, text=column, fg="white", bg="black")
            label.grid(row=i, column=0, pady=5, padx=5)

            entry = tk.Entry(popup, bg="white", fg="black")
            entry.grid(row=i, column=1, pady=5, padx=5)
            if action == "edit" and row_values:
                entry.insert(0, row_values[i])

            entry_widgets.append(entry)

        def save():
            new_values = [entry.get() for entry in entry_widgets]
            now = datetime.now().isoformat()

            if action == "add":
                new_row = dict(zip(self.df.columns, new_values))
                new_row["created_at"] = now
                new_row["updated_at"] = now
                self.df = self.df.append(new_row, ignore_index=True)
            elif action == "edit":
                selected_item = self.tree.selection()[0]
                item_id = int(selected_item)
                for col, value in zip(self.df.columns, new_values):
                    self.df.at[item_id, col] = value
                self.df.at[item_id, "updated_at"] = now

            self.df.to_csv(self.file_path, index_label="id")
            self.render_table()
            popup.destroy()

        save_button = tk.Button(popup, text="Save", command=save, bg="gray", fg="white")
        save_button.grid(row=len(self.df.columns), column=0, columnspan=2, pady=10)

    def search(self):
        search_text = self.search_entry.get().lower()
        if not search_text:
            self.render_table()
            return

        filtered_df = self.df[self.df.apply(lambda row: search_text in row.astype(str).str.lower().values, axis=1)]
        self.render_table(filtered_df)

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        column = self.tree.identify_column(event.x)
        column_index = int(column.replace('#', '')) - 1
        entry_edit = tk.Entry(self.tree, width=20)
        entry_edit.insert(0, self.tree.item(item, 'values')[column_index])
        entry_edit.place(x=event.x, y=event.y)

        def save_edit(event):
            self.tree.set(item, column, entry_edit.get())
            self.update_csv(item, column_index, entry_edit.get())
            entry_edit.destroy()

        entry_edit.bind('<Return>', save_edit)
        entry_edit.focus()

    def update_csv(self, item, column_index, value):
        item_id = int(item)
        column_name = self.df.columns[column_index]
        self.df.at[item_id, column_name] = value
        self.df.at[item_id, "updated_at"] = datetime.now().isoformat()
        self.df.to_csv(self.file_path, index_label="id")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Miia")
    root.geometry("800x600")

    args = sys.argv[1:]
    if not args:
        file_path = "data.csv"
    else:
        file_path = args[0]
    
    app = CSVViewScreen(root, None, file_path)
    app.pack(expand=True, fill='both')
    root.mainloop()