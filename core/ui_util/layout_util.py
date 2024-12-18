def center_window(window, width=None, height=None):
    """
    Center the given window on the screen.
    
    Parameters:
        window (tk.Tk or tk.Toplevel): The window to center.
        width (int, optional): The width of the window. Default is the current width.
        height (int, optional): The height of the window. Default is the current height.
    """
    window.update_idletasks()
    width = width or window.winfo_width()
    height = height or window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')