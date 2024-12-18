from screeninfo import get_monitors
import tkinter as tk

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
    window.geometry(f"{width}x{height}+{x}+{y}")
    
def set_title(window, title):
    window.title(title)
    
def set_dimensions(window, width, height):
    window.geometry(f"{width}x{height}")
    
def set_window_binding(window, key, callback):
    window.bind(key, callback)