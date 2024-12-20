#!/usr/bin/env python3
import os
import tkinter as tk
from gui_components import CSVViewScreen

if __name__ == "__main__":
    default_file_path = os.path.join(os.getcwd(), "default.csv")
    app = tk.Tk()
    CSVViewScreen(app, app, default_file_path).pack(expand=True, fill="both")
    app.title("Miia - CSV Viewer and Editor")
    app.geometry("800x600")
    app.mainloop()
