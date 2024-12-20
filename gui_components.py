import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from datetime import datetime
import os
from csv_utils import generate_default_csv, load_csv

class CSVViewScreen(tk.Frame):
    def __init__(self, parent, app, file_path):
        super().__init__(parent)
        self.app = app
        self.file_path = file_path

        # Undo/Redo stacks
        self.undo_stack = []
        self.redo_stack = []

        if not os.path.exists(self.file_path):
            generate_default_csv(self.file_path)

        self.df = pd.DataFrame()
        self.setup_ui()

    def setup_ui(self):
        self.configure(bg="black")
        # Title Label
        title_label = tk.Label(self, text="Miia", fg="white", bg="black", font=("Arial", 16))
        title_label.pack(pady=10)

        # Search Bar
        search_frame = tk.Frame(self, bg="black")
        search_frame.pack(pady=5)
        search_label = tk.Label(search_frame, text="Search:", fg="white", bg="black")
        search_label.pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        # Search Dropdown for columns
        self.column_filter = ttk.Combobox(search_frame, state="readonly")
        self.column_filter.pack(side=tk.LEFT, padx=5)
        self.column_filter.set("All Columns")

        search_button = tk.Button(search_frame, text="Search", command=self.search, bg="gray", fg="white")
        search_button.pack(side=tk.LEFT, padx=5)

        # Treeview Styling
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground="black", fieldbackground="white")

        # Treeview Table
        self.tree = ttk.Treeview(self, show='headings')
        self.tree.pack(expand=True, fill='both', pady=10, padx=10)
        self.tree.bind('<Double-1>', self.on_double_click)

        # Load CSV Data
        self.load_csv()

        # Buttons
        button_frame = tk.Frame(self, bg="black")
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, text="Add", command=self.add_row, bg="gray", fg="white")
        add_button.pack(side=tk.LEFT, padx=5)

        edit_button = tk.Button(button_frame, text="Edit", command=self.edit_row, bg="gray", fg="white")
        edit_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(button_frame, text="Delete", command=self.delete_row, bg="gray", fg="white")
        delete_button.pack(side=tk.LEFT, padx=5)

        undo_button = tk.Button(button_frame, text="Undo", command=self.undo, bg="gray", fg="white")
        undo_button.pack(side=tk.LEFT, padx=5)

        redo_button = tk.Button(button_frame, text="Redo", command=self.redo, bg="gray", fg="white")
        redo_button.pack(side=tk.LEFT, padx=5)

        import_button = tk.Button(button_frame, text="Import CSV", command=self.import_csv, bg="gray", fg="white")
        import_button.pack(side=tk.LEFT, padx=5)

        export_button = tk.Button(button_frame, text="Export to Excel", command=self.export_to_excel, bg="gray", fg="white")
        export_button.pack(side=tk.LEFT, padx=5)

    def load_csv(self):
        try:
            self.df = load_csv(self.file_path)
            self.render_table()
            self.column_filter["values"] = ["All Columns"] + list(self.df.columns)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file: {e}")

    def render_table(self, df=None):
        self.tree.delete(*self.tree.get_children())
        if df is None:
            df = self.df

        self.tree["columns"] = list(df.columns)
        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for index, row in df.iterrows():
            self.tree.insert("", "end", iid=index, values=list(row))

    def add_row(self):
        self.show_edit_popup(action="add")

    def edit_row(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a row to edit.")
            return

        row_values = self.tree.item(selected_item[0], "values")
        self.show_edit_popup(action="edit", row_values=row_values)

    def delete_row(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a row to delete.")
            return

        item_id = int(self.tree.selection()[0])
        self.undo_stack.append(self.df.copy())
        self.df = self.df.drop(item_id)
        self.df.to_csv(self.file_path, index_label="id")
        self.render_table()

    def on_double_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        row_values = self.tree.item(selected_item[0], "values")
        self.show_edit_popup(action="edit", row_values=row_values)

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

            self.undo_stack.append(self.df.copy())
            if action == "add":
                new_row = dict(zip(self.df.columns, new_values))
                new_row["created_at"] = now
                new_row["updated_at"] = now
                new_row_df = pd.DataFrame([new_row], columns=self.df.columns)
                self.df = pd.concat([self.df, new_row_df], ignore_index=True)
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
        column_filter = self.column_filter.get()

        if not search_text:
            self.render_table()
            return

        if column_filter == "All Columns":
            filtered_df = self.df[self.df.apply(lambda row: search_text in row.astype(str).str.lower().values, axis=1)]
        else:
            filtered_df = self.df[self.df[column_filter].astype(str).str.lower().str.contains(search_text, na=False)]

        self.render_table(filtered_df)

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.df.copy())
            self.df = self.undo_stack.pop()
            self.df.to_csv(self.file_path, index_label="id")
            self.render_table()
        else:
            messagebox.showinfo("Undo", "No actions to undo.")

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.df.copy())
            self.df = self.redo_stack.pop()
            self.df.to_csv(self.file_path, index_label="id")
            self.render_table()
        else:
            messagebox.showinfo("Redo", "No actions to redo.")

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                imported_df = pd.read_csv(file_path)
                self.undo_stack.append(self.df.copy())
                self.df = pd.concat([self.df, imported_df], ignore_index=True)
                self.df.to_csv(self.file_path, index_label="id")
                self.render_table()
                messagebox.showinfo("Import", "CSV file imported successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import CSV file: {e}")

    def export_to_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                self.df.to_excel(file_path, index_label="id")
                messagebox.showinfo("Export", "Data exported to Excel successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data to Excel: {e}")
