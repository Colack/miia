#!/usr/bin/env python3
"""
============================
Miia - CSV Viewer and Editor
============================

A Python application using Tkinter to create a GUI for viewing and editing CSV files.

Dev Notes:
    This took me about three days to complete, and required a lot of research and trial and error to get everything working as expected.
    The most challenging part was figuring out how to implement inline editing for the Treeview table, as there is no built-in support for it.
    Hopefully this code will be helpful to others who are looking to build similar applications using Tkinter and Pandas.
    
    I have tested this code on Arch Linux with Python, so I'm not sure if it will work on Windows or MacOS without any modifications.
    Please let me know if you encounter any issues or have any suggestions for improvements.
    
    Thanks,
    ~ Jack Spencer ~

Version: 0.1
License: MIT
GitHub: github.com/colack/miia

Features:
- Create a default CSV if none exists.
- View, search, add, edit, and delete rows.
- Dark and light mode styling for enhanced UI.
- Real-time inline editing.

"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
import sys
from datetime import datetime

class CSVViewScreen(tk.Frame):
    """
    A class to represent the main application screen for viewing and editing CSV files.

    Attributes:
    ----------
    parent : tk.Widget
        The parent widget for this frame.
    app : object
        Reference to the main application instance.
    file_path : str
        The path to the CSV file being managed.
    df : pandas.DataFrame
        The dataframe storing the CSV data.
    """

    def __init__(self, parent, app, file_path):
        """
        Initialize the CSVViewScreen class.

        Parameters:
        ----------
        parent : tk.Widget
            The parent widget.
        app : object
            Main application instance.
        file_path : str
            Path to the CSV file.
        """
        super().__init__(parent)
        self.app = app
        self.file_path = file_path

        if not os.path.exists(self.file_path):
            self.generate_default_csv()

        self.df = pd.DataFrame()
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface elements.
        """
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
        search_button = tk.Button(search_frame, text="Search", command=self.search, bg="gray", fg="white")
        search_button.pack(side=tk.LEFT, padx=5)

        # Treeview Styling
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        fieldbackground="white")

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

    def generate_default_csv(self):
        """
        Generate a default CSV file if one does not exist.
        """
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
        """
        Load the CSV file into a Pandas DataFrame and populate the Treeview table.
        """
        try:
            self.df = pd.read_csv(self.file_path, index_col="id")
            self.df["price"] = pd.to_numeric(self.df["price"], errors="coerce")
            self.df["discount"] = pd.to_numeric(self.df["discount"], errors="coerce")
            self.df["created_at"] = pd.to_datetime(self.df["created_at"], errors="coerce")
            self.df["updated_at"] = pd.to_datetime(self.df["updated_at"], errors="coerce")
            self.render_table()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file: {e}")

    def render_table(self, df=None):
        """
        Populate the Treeview table with data from the DataFrame.

        Parameters:
        ----------
        df : pandas.DataFrame, optional
            The dataframe to render. Defaults to the main dataframe.
        """
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
        """
        Add a new row to the table.
        """
        self.show_edit_popup(action="add")

    def edit_row(self):
        """
        Edit the selected row in the table.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a row to edit.")
            return

        row_values = self.tree.item(selected_item[0], "values")
        self.show_edit_popup(action="edit", row_values=row_values)

    def delete_row(self):
        """
        Delete the selected row from the table.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a row to delete.")
            return

        item_id = int(self.tree.selection()[0])
        self.df = self.df.drop(item_id)
        self.df.to_csv(self.file_path, index_label="id")
        self.render_table()

    def show_edit_popup(self, action, row_values=None):
        """
        Display a popup window for editing or adding rows.

        Parameters:
        ----------
        action : str
            Either "add" or "edit".
        row_values : list, optional
            Values of the selected row (for editing).
        """
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
        """
        Search the DataFrame for matching text and display results in the table.
        """
        search_text = self.search_entry.get().lower()
        if not search_text:
            self.render_table()
            return

        filtered_df = self.df[self.df.apply(lambda row: search_text in row.astype(str).str.lower().values, axis=1)]
        self.render_table(filtered_df)

    def on_double_click(self, event):
        """
        Enable inline editing of cells in the Treeview table.
        """
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if not item or column == "#0":
            return

        column_index = int(column.replace("#", "")) - 1
        entry_edit = tk.Entry(self.tree, width=20)
        entry_edit.insert(0, self.tree.item(item, "values")[column_index])
        entry_edit.place(x=event.x, y=event.y)

        def save_edit(event):
            new_value = entry_edit.get()
            self.tree.set(item, column, new_value)
            self.update_csv(item, column_index, new_value)
            entry_edit.destroy()

        entry_edit.bind("<Return>", save_edit)
        entry_edit.bind("<FocusOut>", save_edit)
        entry_edit.focus()

    def update_csv(self, item, column_index, value):
        """
        Update the DataFrame and save changes to the CSV file after editing a cell.
        
        Parameters:
        ----------
        item : str
            The ID of the row in the Treeview.
        column_index : int
            The index of the column being edited.
        value : str
            The new value to update.
        """
        item_id = int(item)
        column_name = self.df.columns[column_index]
        self.df.at[item_id, column_name] = value
        self.df.at[item_id, "updated_at"] = datetime.now().isoformat()
        self.df.to_csv(self.file_path, index_label="id")

if __name__ == "__main__":
    """
    Main entry point of the application.
    """
    root = tk.Tk()
    root.title("Miia")
    root.geometry("800x600")

    args = sys.argv[1:]
    file_path = args[0] if args else "data.csv"

    app = CSVViewScreen(root, None, file_path)
    app.pack(expand=True, fill='both')
    root.mainloop()
