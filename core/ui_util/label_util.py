import tkinter as tk
from tkinter import ttk

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