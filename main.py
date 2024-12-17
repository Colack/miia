import sys
import os
from dotenv import load_dotenv
from core.ui import AutoShopApp
import ttkbootstrap as tb

def main():
    # Load environment variables
    load_dotenv()
    csv_file_path = os.getenv("CSV_FILE_PATH", "orders.csv")
    debug_mode = os.getenv("DEBUG_MODE", "False").lower() == "true"
    
    # Handle CLI arguments
    new_csv_mode = "--new" in sys.argv
    if new_csv_mode:
        from core.order_manager import create_csv_file
        create_csv_file(csv_file_path)
        print("New CSV file created with required fields.")
        sys.exit()

    # Load default theme
    theme = os.getenv("DEFAULT_THEME", "darkly")

    # Initialize application
    root = tb.Window(themename=theme)
    app = AutoShopApp(root, debug_mode)
    root.mainloop()

if __name__ == "__main__":
    main()
