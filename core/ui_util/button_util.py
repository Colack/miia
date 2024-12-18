import tkinter as tk
from tkinter import ttk

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