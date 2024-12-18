#!/usr/bin/env python3
"""
    Miia v0.1.0
    (c) 2024 by Jack Spencer
    
    This is a tkinter program to edit, modify, and update CSV tables.
"""

#####
# Importing the necessary modules
#####

import os
import json
import logging
import tkinter as tk
import ttkbootstrap as tb
import sys
import time
import csv
import bcrypt

from dotenv import load_dotenv
from tkinter import ttk, messagebox
from screeninfo import get_monitors

#####
# Global Variables
#####

debug_mode = False
version = "0.1.0"

#####
# Debug mode uses the logging module to output debug messages
#####
if debug_mode:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
else:
    logging.basicConfig(level=logging.WARNING)
    
#####
# File Manager Class
#####

class FileManager:
    # Initialize the FileManager
    def __init__(self, data_folder="data"):
        logging.debug(f"Initializing FileManager with data folder: {data_folder}") # Debugging
        self.data_folder = data_folder
        self.metadata_file = os.path.join(data_folder, "metadata.json")
        self.ensure_data_folder()
        self.load_metadata()
        
    # Ensure the data folder exists
    def ensure_data_folder(self):
        logging.debug(f"Ensuring data folder exists: {self.data_folder}") # Debugging
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
            logging.debug(f"Created data folder: {self.data_folder}") # Debugging
            
    # Load the metadata file
    def load_metadata(self):
        try:
            with open(self.metadata_file, "r") as file:
                self.metadata = json.load(file)
                logging.debug(f"Loaded metadata file: {self.metadata_file}") # Debugging
        except FileNotFoundError:
            self.metadata = {}
            self.save_metadata()
            logging.debug(f"Metadata file not found: {self.metadata_file}")
            
    # Save the metadata file
    def save_metadata(self):
        with open(self.metadata_file, "w") as file:
            json.dump(self.metadata, file, indent=4)
            logging.debug(f"Saved metadata file: {self.metadata_file}") # Debugging
            
    # Create a csv file
    def create_csv(self, name, fields):
        logging.debug(f"Creating CSV file: {name}") # Debugging
        
        # Check if fields are empty
        if not fields or not all(fields):
            logging.error("Fields are empty") # Debugging
            return False
        
        # Create the file path
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        
        # Check if the file already exists
        if name in self.metadata:
            logging.error(f"CSV file already exists: {name}") # Debugging
            return False
        
        # Check for duplicate fields
        if len(fields) != len(set(fields)):
            logging.error("Duplicate fields") # Debugging
            return False
        
        # Write the fields to the file
        with open(file_path, "w") as file:
            writer = csv.writer(file)
            writer.writerow(fields)
            logging.debug(f"Wrote fields to CSV file: {file_path}") # Debugging
            
        # Update the metadata
        self.metadata[name] = fields
        
        # Save the metadata
        self.save_metadata()
        
        return file_path
    
    # List all csv files
    def list_csv(self):
        logging.debug("Listing CSV files") # Debugging
        return [name for name in self.metadata]

    # Get the fields of a csv file
    def get_fields(self, name):
        logging.debug(f"Getting fields of CSV file: {name}") # Debugging
        return self.metadata.get(name, [])
    
    # Read a csv file
    def read_csv(self, name):
        logging.debug(f"Reading CSV file: {name}") # Debugging
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            logging.error(f"CSV file does not exist: {name}") # Debugging
            return []
        
        # Read the file
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            data = [row for row in reader]
            logging.debug(f"Read CSV file: {file_path}") # Debugging
            return data
        
    # Write to a csv file
    def write_csv(self, name, data):
        logging.debug(f"Writing to CSV file: {name}") # Debugging
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        
        # Write to the file
        with open(file_path, "w") as file:
            writer = csv.writer(file)
            writer.writerows(data)
            logging.debug(f"Wrote to CSV file: {file_path}") # Debugging
            
    # Delete a csv file
    def delete_csv(self, name):
        logging.debug(f"Deleting CSV file: {name}") # Debugging
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            logging.error(f"CSV file does not exist: {name}") # Debugging
            return False
        
        # Delete the file
        os.remove(file_path)
        logging.debug(f"Deleted CSV file: {file_path}") # Debugging
        
        # Delete the metadata
        del self.metadata[name]
        
        # Save the metadata
        self.save_metadata()
        
        return True
    
    # Rename a csv file
    def rename_csv(self, name, new_name):
        logging.debug(f"Renaming CSV file: {name} to {new_name}") # Debugging
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        new_file_path = os.path.join(self.data_folder, f"{new_name}.csv")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            logging.error(f"CSV file does not exist: {name}") # Debugging
            return False
        
        # Check if the new name already exists
        if new_name in self.metadata:
            logging.error(f"CSV file already exists: {new_name}") # Debugging
            return False
        
        # Rename the file
        os.rename(file_path, new_file_path)
        logging.debug(f"Renamed CSV file: {file_path} to {new_file_path}") # Debugging
        
        # Update the metadata
        self.metadata[new_name] = self.metadata[name]
        del self.metadata[name]
        
        # Save the metadata
        self.save_metadata()
        
        return True
    
    # Add a row to a csv file
    def add_row(self, name, row):
        logging.debug(f"Adding row to CSV file: {name}") # Debugging
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            logging.error(f"CSV file does not exist: {name}") # Debugging
            return False
        
        # Read the file
        data = self.read_csv(name)
        
        # Add the row
        data.append(row)
        
        # Write to the file
        self.write_csv(name, data)
        
        return True
    
    # Update a row in a csv file
    def update_row(self, name, index, row):
        logging.debug(f"Updating row in CSV file: {name}") # Debugging
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            logging.error(f"CSV file does not exist: {name}") # Debugging
            return False
        
        # Read the file
        data = self.read_csv(name)
        
        # Update the row
        data[index] = row
        
        # Write to the file
        self.write_csv(name, data)
        
        return True
    
    # Delete a row from a csv file
    def delete_row(self, name, index):
        logging.debug(f"Deleting row from CSV file: {name}") # Debugging
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            logging.error(f"CSV file does not exist: {name}") # Debugging
            return False
        
        # Read the file
        data = self.read_csv(name)
        
        # Delete the row
        del data[index]
        
        # Write to the file
        self.write_csv(name, data)
        
        return True
    
    # Search for a row in a csv file
    def search_row(self, name, field, value):
        logging.debug(f"Searching for row in CSV file: {name}") # Debugging
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            logging.error(f"CSV file does not exist: {name}") # Debugging
            return None
        
        # Read the file
        data = self.read_csv(name)
        
        # Search for the row
        for index, row in enumerate(data):
            if row[field] == value:
                return index, row
            
        return None
    
    # Search for rows in a csv file
    def search_rows(self, name, field, value):
        logging.debug(f"Searching for rows in CSV file: {name}") # Debugging
        file_path = os.path.join(self.data_folder, f"{name}.csv")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            logging.error(f"CSV file does not exist: {name}") # Debugging
            return []
        
        # Read the file
        data = self.read_csv(name)
        
        # Search for the rows
        rows = []
        for index, row in enumerate(data):
            if row[field] == value:
                rows.append((index, row))
                
        return rows

    # Create a backup of the data folder
    def backup(self, folder="backup"):
        logging.debug(f"Creating backup of data folder: {folder}") # Debugging
        backup_folder = os.path.join(self.data_folder, folder)
        self.ensure_data_folder()
        
        # Check if the backup folder already exists
        if os.path.exists(backup_folder):
            logging.error(f"Backup folder already exists: {folder}") # Debugging
            return False
        
        # Copy the data folder to the backup folder
        os.system(f"cp -r {self.data_folder} {backup_folder}")
        logging.debug(f"Created backup of data folder: {folder}") # Debugging
        
        return True
    
#####
# User Manager Class
#####

class UserManager:
    def __init__(self, user_file="data/users.json"):
        self.user_file = user_file
        self.load_users()
        
    def load_users(self):
        if os.path.exists(self.user_file):
            with open(self.user_file, "r") as file:
                self.users = json.load(file)
        else:
            self.users = {}
            
    def save_users(self):
        with open(self.user_file, "w") as file:
            json.dump(self.users, file, indent=4)
            
    def register_user(self, username, password):
        if username in self.users:
            logging.warning(f"User {username} already exists")
            return False
        
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self.users[username] = {
            "password": hashed_password,
            "role": "user"
        }
        self.save_users()
        
    def login_user(self, username, password):
        if username not in self.users:
            logging.warning(f"User {username} does not exist")
            return False
        
        hashed_password = self.users[username]["password"]
        if bcrypt.checkpw(password.encode(), hashed_password.encode()):
            return True
        else:
            return False
        
    def change_password(self, username, old_password, new_password):
        if username not in self.users:
            logging.warning(f"User {username} does not exist")
            return False
        
        hashed_password = self.users[username]["password"]
        if bcrypt.checkpw(old_password.encode(), hashed_password.encode()):
            new_hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            self.users[username]["password"] = new_hashed_password
            self.save_users()
            return True
        else:
            return False
        
    # NOTE: This function is only for Administrators, please don't use it for regular users
    def change_role(self, username, role):
        if username not in self.users:
            logging.warning(f"User {username} does not exist")
            return False
        
        self.users[username]["role"] = role
        self.save_users()
        return True
    
    def delete_user(self, username):
        if username not in self.users:
            logging.warning(f"User {username} does not exist")
            return False
        
        del self.users[username]
        self.save_users()
        return True
    
    def get_users(self):
        return self.users
    
    def get_user(self, username):
        if username in self.users:
            return self.users[username]
        else:
            return None
        
    def get_roles(self):
        return ["user", "admin"]
    
    def is_admin(self, username):
        if username in self.users:
            return self.users[username]["role"] == "admin"
        else:
            return False
        
    def is_user(self, username):
        if username in self.users:
            return self.users[username]["role"] == "user"
        else:
            return False
        
    def is_valid_role(self, role):
        return role in self.get_roles()
    
    def is_valid_user(self, username):
        return username in self.users

# Miia Main Application Class
class Miia:
    def __init__(self, root, debug_mode, title, version):
        self.title = title
        self.version = version
        self.root = root
        self.debug_mode = debug_mode
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

#####
# Login Screen
#####
class LoginScreen(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app
        self.user_manager = UserManager()
        self.setup_ui()
        
    def setup_ui(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        create_label(self, "Username")
        self.username_entry = create_entry(self, textvariable=self.username_var)
        
        create_label(self, "Password")
        self.password_entry = create_entry(self, textvariable=self.password_var, show="*")
        
        self.login_button = create_button(self, "Login", self.login)
        self.register_button = create_button(self, "Register", self.register)
        
    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        if self.user_manager.login_user(username, password):
            messagebox.showinfo("Login", "Login successful")
        else:
            messagebox.showerror("Login", "Login failed")
            
    def register(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        self.user_manager.register_user(username, password)
        messagebox.showinfo("Register", "User registered")
        

# Utility Functions
def create_button(parent, text, command, **kwargs):
    """
    Create a button with the given text and command.
    
    Parameters:
        parent (tk.Widget): The parent widget.
        text (str): The text to display on the button.
        command (function): The function to call when the button is clicked.
        **kwargs: Additional keyword arguments to pass to the Button constructor.
    
    Returns:
        ttk.Button: The created button.
    """
    button = ttk.Button(parent, text=text, command=command, **kwargs)
    button.pack(pady=5)
    return button

def create_entry(parent, textvariable=None, **kwargs):
    """
    Create an entry widget with the given textvariable.

    Parameters:
        parent (tk.Widget): The parent widget.
        textvariable (tk.StringVar, optional): The variable to store the entry text.
        **kwargs: Additional keyword arguments to pass to the Entry constructor.

    Returns:
        ttk.Entry: The created entry widget.
    """
    entry = ttk.Entry(parent, textvariable=textvariable, **kwargs)
    entry.pack(pady=5)
    return entry

def create_label(parent, text, **kwargs):
    """
    Create a label with the given text.
    
    Parameters:
        parent (tk.Widget): The parent widget.
        text (str): The text to display on the label.
        **kwargs: Additional keyword arguments to pass to the Label constructor.
    
    Returns:
        ttk.Label: The created label.
    """
    label = ttk.Label(parent, text=text, **kwargs)
    label.pack(pady=5)
    return label

def center_window(window, width=None, height=None):
    """
    Center a window on the screen.
    
    Parameters:
        window (tk.Tk): The window to center.
        width (int, optional): The width of the window.
        height (int, optional): The height of the window.
    """
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    if not width:
        width = window.winfo_width()
    if not height:
        height = window.winfo_height()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
    
def get_screen_width():
    return get_monitors()[0].width

def get_screen_height():
    return get_monitors()[0].height

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')
    
def set_title(window, title):
    window.title(title)
    
def set_dimensions(window, width, height):
    window.geometry(f"{width}x{height}")
    
def set_window_binding(window, key, command):
    window.bind(key, command)
    
#####
# Main Function
#####

def main():
    """
    The main function initializes the application.
    It loads environment variables, sets the theme, and starts the main application loop.
    """
    # Load environment variables
    load_dotenv()
    
    # Load default theme from environment variables or use "darkly" as default
    theme = os.getenv("DEFAULT_THEME", "darkly")
    
    # Initialize the application window with the specified theme
    root = tb.Window(themename=theme)
    
    # Create an instance of the Miia class
    app = Miia(root, debug_mode, "Miia", version)
    
    # Start the Tkinter main loop
    root.mainloop()
    
if __name__ == "__main__":
    main()