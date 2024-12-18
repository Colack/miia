import tkinter as tk
from tkinter import ttk

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