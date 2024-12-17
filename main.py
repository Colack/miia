import sys
from core.ui import AutoShopApp
import ttkbootstrap as tb

def main():
    csv_file_path = "orders.csv"
    debug_mode = "--debug" in sys.argv
    new_csv_mode = "--new" in sys.argv

    if new_csv_mode:
        from core.order_manager import create_csv_file
        create_csv_file(csv_file_path)
        print("New CSV file created with required fields.")
        sys.exit()

    root = tb.Window(themename="darkly")
    app = AutoShopApp(root, csv_file_path, debug_mode)
    root.mainloop()

if __name__ == "__main__":
    main()
